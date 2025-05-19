# my_ibslabs_blockchain/models/account_move.py
import base64
import pprint
import tempfile
import json
import secrets
from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    blockchain_evidence_id        = fields.Char(string="Blockchain Evidence ID", copy=False)
    blockchain_evidence_data = fields.Text(string="Evidence Data", readonly=True, copy=False)
    blockchain_status        = fields.Char(string="Evidence Status", copy=False, tracking=True)
    blockchain_webhook_data = fields.Text(string="Webhook Data", readonly=True, copy=False, tracking=True)
    blockchain_checker_url = fields.Char(string="Checker URL", copy=False, tracking=True)

    def action_sign_blockchain(self):
        self = self.sudo()
        self.ensure_one()

        signature_id = self.env['ir.config_parameter'].sudo().get_param('icommunity.signature_id', "sig_RKDEPgYSqRpNStQA6Vyfgw")
        if not signature_id:
            raise UserError("Parámetro icommunity.signature_id no está definido")


        invoice_pdf_content = self.env['ir.actions.report'].with_context(force_report_rendering=True)._render_qweb_pdf(
            'account.report_invoice_with_payments',
            self.ids)[0]

        pdf_b64 = invoice_pdf_content
        if not pdf_b64:
            raise UserError("No se encontró invoice_pdf_report_file para esta factura.")
        #
        tmp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        tmp.write(pdf_b64)
        tmp.flush()
        tmp.close()
        fname = tmp.name

        files = [
            {
                'name': f"{fname}",  # Nombre del archivo
                'file': base64.b64encode(pdf_b64).decode('utf-8')  # Contenido en base64
            }
        ]

        # pass contraseña: umnncrN5g4tqCN@
        signature_ids = ["sig_RKDEPgYSqRpNStQA6Vyfgw"]

        evidencia = self.env['icommunity.api.client'].create_evidence(
            title=self.name,  # ponemos el nombre de la factura
            files=files,
            signature_ids=signature_ids
        )
        # print(evidencia)

        # lo hacemos aqui via python:
        evidencia_id = evidencia.get('id')

        # self.blockchain_evidence_data = pprint.pformat(evidencia, indent=4)
        # self.blockchain_evidence_id = evidencia_id
        # self.blockchain_status = evidencia.get('status', '')
        self.write({
            'blockchain_evidence_data': pprint.pformat(evidencia, indent=4),
            'blockchain_evidence_id': evidencia_id,
            'blockchain_status': evidencia.get('status', ''),
        })

        return True
