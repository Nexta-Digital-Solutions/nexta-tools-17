# my_ibslabs_blockchain/models/account_move.py
import base64
import pprint
import tempfile
import json
import secrets
from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class HRAttendance(models.Model):
    _inherit = 'hr.attendance'

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

        # pass contraseña: umnncrN5g4tqCN@
        signature_ids = ["sig_RKDEPgYSqRpNStQA6Vyfgw"]

        attendance_data = {
            'attendance_id': self.id,
            'employee_id': self.employee_id.id,
            'employee_name': self.employee_id.name,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'worked_hours': self.worked_hours,
            'display_name': self.display_name,
            'create_date': self.create_date,
        }

        file_generado_al_vuelo = {
            'name': f"{self.display_name}.json",  # Nombre del archivo
            'file': base64.b64encode(str(attendance_data).encode('utf-8')).decode('utf-8')  # Contenido en base64
        }

        evidencia = self.env['icommunity.api.client'].create_evidence(
            title=self.display_name,  # ponemos el nombre de la factura
            files=[file_generado_al_vuelo],
            signature_ids=signature_ids
        )

        evidencia_id = evidencia.get('id')

        self.write({
            'blockchain_evidence_data': pprint.pformat(evidencia, indent=4),
            'blockchain_evidence_id': evidencia_id,
            'blockchain_status': evidencia.get('status', 'evidence.created'),
        })

        return True



    def action_sign_blockchain_bulk(self):
        for attendance in self:
            try:
                attendance.action_sign_blockchain()
            except UserError as e:
                _logger.error(f"Error signing attendance {attendance.id} on blockchain: {e}")
                continue