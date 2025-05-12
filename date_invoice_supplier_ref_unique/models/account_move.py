# Copyright 2024 Jaume Basiero Herrero Nextads
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_date = fields.Date(string='Invoice/Bill Date', readonly=True, index=True, copy=False,
                               states={'draft': [('readonly', False)]})
    @api.constrains("supplier_invoice_number")
    def _check_unique_supplier_invoice_number_insensitive(self):
        for rec in self:
            if rec.supplier_invoice_number and rec.is_purchase_document(include_receipts=True):
                if rec.invoice_date:
                    invoice_year = rec.invoice_date.year
                same_supplier_inv_num = rec.search(
                    [
                        ("commercial_partner_id", "=", rec.commercial_partner_id.id),
                        ("move_type", "in", ("in_invoice", "in_refund")),
                        (
                            "supplier_invoice_number",
                            "=ilike",
                            rec.supplier_invoice_number,
                        ),
                        ("id", "!=", rec.id),
                    ],
                    limit=1,
                )
                for invoice in same_supplier_inv_num:
                    if rec.invoice_date:
                        current_invoice_year = invoice.invoice_date.year
                        if invoice_year and current_invoice_year and invoice_year == current_invoice_year:
                            raise ValidationError(
                                _(
                                    "The invoice/refund with supplier invoice number '%s' "
                                    "already exists in Odoo under the number '%s' "
                                    "for supplier '%s' in the same year '%s'."
                                )
                                % (
                                    same_supplier_inv_num.supplier_invoice_number,
                                    same_supplier_inv_num.name or "-",
                                    same_supplier_inv_num.partner_id.display_name,
                                    current_invoice_year
                                )
                            )
