# Copyright 2004-2009 Tiny SPRL (<http://tiny.be>).
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# Copyright 2015-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _add_supplier_to_product(self):
        """Insert a mapping of products to PO lines to be picked up
        in supplierinfo's create()"""
        self.ensure_one()
        po_line_map = {
            line.product_id.product_tmpl_id.id: line for line in self.order_line
        }
        return super(
            PurchaseOrder, self.with_context(po_line_map=po_line_map)
        )._add_supplier_to_product()


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # adding discount to depends
    # Se comenta por que esta duplicando el calculo del descuento
    #@api.depends("discount")
    #def _compute_amount(self):
    #    return super()._compute_amount()

    def _convert_to_tax_base_line_dict(self):
        # Inject the new price_unit with discount if there's any. There's an specific
        # value in the dictionary for the discount, but we need to include it in the
        # price unit for the stock move price unit valuation to be correct
        vals = super()._convert_to_tax_base_line_dict()
        #Se comenta por que esta duplicando el calculo del descuento
        #vals["price_unit"] = self._get_discounted_price_unit()
        return vals

    discount = fields.Float(string="Discount (%)", digits="Discount")

    _sql_constraints = [
        (
            "discount_limit",
            "CHECK (discount <= 100.0)",
            "Discount must be lower than 100%.",
        )
    ]

    def _get_discounted_price_unit(self):
        """Inheritable method for getting the unit price after applying
        discount(s).

        :rtype: float
        :return: Unit price after discount(s).
        """
        self.ensure_one()
        if self.discount:
            return self.price_unit * (1 - self.discount / 100)
        return self.price_unit

    def _compute_price_unit_and_date_planned_and_name(self):
        """Get also the discount from the seller. Unfortunately, this requires to
        select again the seller to be used, as there isn't any hook to use the already
        selected one.
        """
        res = super()._compute_price_unit_and_date_planned_and_name()
        for line in self.filtered("product_id"):
            seller = line.product_id._select_seller(
                partner_id=line.partner_id,
                quantity=line.product_qty,
                date=line.order_id.date_order
                and line.order_id.date_order.date()
                or fields.Date.context_today(line),
                uom_id=line.product_uom,
                params={"order_id": line.order_id},
            )
            line._apply_value_from_seller(seller)
        return res

    @api.model
    def _apply_value_from_seller(self, seller):
        """Overload this function to prepare other data from seller,
        like in purchase_triple_discount module"""
        if not seller:
            return
        self.discount = seller.discount

    def _prepare_account_move_line(self, move=False):
        vals = super()._prepare_account_move_line(move)
        if self.env["account.move.line"]._fields.get("discount1", False):
            # OCA/account_invoice_triple_discount is installed
            vals["discount1"] = self.discount
        else:
            vals["discount"] = self.discount
        return vals

    @api.model
    def _prepare_purchase_order_line(
        self, product_id, product_qty, product_uom, company_id, supplier, po
    ):
        """Apply the discount to the created purchase order"""
        res = super()._prepare_purchase_order_line(
            product_id, product_qty, product_uom, company_id, supplier, po
        )
        partner = supplier.partner_id
        uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
        seller = product_id.with_company(company_id)._select_seller(
            partner_id=partner,
            quantity=uom_po_qty,
            date=po.date_order and po.date_order.date(),
            uom_id=product_id.uom_po_id,
        )
        res.update(self._prepare_purchase_order_line_from_seller(seller))
        return res

    @api.model
    def _prepare_purchase_order_line_from_seller(self, seller):
        """Overload this function to prepare other data from seller,
        like in purchase_triple_discount module"""
        if not seller:
            return {}
        return {"discount": seller.discount}

    def write(self, vals):
        res = super().write(vals)
        if "discount" in vals or "price_unit" in vals:
            for line in self.filtered(lambda l: l.order_id.state == "purchase"):
                # Avoid updating kit components' stock.move
                moves = line.move_ids.filtered(
                    lambda s: s.state not in ("cancel", "done")
                    and s.product_id == line.product_id
                )
                moves.write({"price_unit": line._get_discounted_price_unit()})
        return res
