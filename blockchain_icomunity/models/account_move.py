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


        client = self.env['icommunity.api.client'].create({})

        invoice_pdf_content = self.env['ir.actions.report'].with_context(force_report_rendering=True)._render_qweb_pdf(
            'account.report_invoice_with_payments',
            self.ids)[0]

        # pdf_b64 = self.invoice_pdf_report_file
        pdf_b64 = invoice_pdf_content
        if not pdf_b64:
            raise UserError("No se encontró invoice_pdf_report_file para esta factura.")
        pdf_bytes = base64.b64decode(pdf_b64)
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
        print(evidencia)

        # lo hacemos aqui via python:
        evidencia_id = evidencia.get('id')

        self.blockchain_evidence_data = pprint.pformat(evidencia, indent=4)
        self.blockchain_evidence_id = evidencia_id
        self.blockchain_status = evidencia.get('status', '')
        # d = {
        #     "created_at": "2025-05-19T14:40:16.13927Z",
        #     "id": "evd_oHNYBLkziikZkEZXdZLKQd",
        #     "title": "INV/2025/00002",
        #     "status": "waiting",
        #     "certification": {
        #         "links": {}
        #     },
        #     "payload": {},
        #     "signature": [
        #         {"name": "nextads_test_signature", "id": "sig_RKDEPgYSqRpNStQA6Vyfgw",
        #          "sources": [{"id": "QmVDgkBycXDYpakUnJh9XsE6TQ9Dq6KG891G8ANS3d1eBC",
        #                       "name": "nextads_test_signature",
        #                       "provider": "ipfs",
        #      "integrity": [{"name": "Back.jpg", "type": "file", "checksum": "RTM0JRO1jJona4T956Yq5xdp+WD4FY6R+u7l//Zl7l29aPbFXjwrP4aQAY/b05OAYwGNv56xcU6wpokMtSYwAg==", "algorithm": "SHA-512", "sanitizer": "base64.standard"},
        #                    {"name": "Selfie.jpg", "type": "file", "checksum": "U0oQpn3kkcRq7XM9lbvcIicUqSih2KNpq2s4acy4afmw1Fr3+ehvWlUDAZDaMiQZOvOK1NJ+FzFRgrptWcEpSA==", "algorithm": "SHA-512", "sanitizer": "base64.standard"},
        #                    {"name": "Front.jpg", "type": "file", "checksum": "Eqab9ZMMC3nhKHTI8GbaPAeEOZvfMqoSP/wiNdzMLClL559ageSxticqTrbYMEjQIG5F5RPQIHKQVvXvozz6Qw==", "algorithm": "SHA-512", "sanitizer": "base64.standard"}], "made_by_ibs": true}]}]}


        # # y con los datos de respuesta completamos los campos:
        # self.blockchain_pdf_id        = pdf_id
        # self.blockchain_status        = checker
        # self.blockchain_certification = json.dumps(data.get('certification', {}), indent=2)

        return True
