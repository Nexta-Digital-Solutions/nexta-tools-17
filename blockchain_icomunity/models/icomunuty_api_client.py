# my_ibslabs_blockchain/models/icommunity_api.py
import os
import logging
import requests
from odoo import models, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ICommunityAPIClient(models.TransientModel):
    _name = 'icommunity.api.client'
    _description = 'iCommunity Labs API Client'

    @api.model
    def _get_base_url(self):
        url = self.env['ir.config_parameter'].sudo().get_param('icommunity.api_base_url')
        if not url:
            raise UserError("Parámetro icommunity.api_base_url no está configurado")
        return url

    @api.model
    def _get_headers(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('icommunity.api_key')
        if not api_key:
            raise UserError("Parámetro icommunity.api_key no está configurado")
        ret = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json',
        }
        return ret

    @api.model
    def create_evidence(self, title, files, signature_ids):
        """
        Crea una nueva evidencia en el API de iCommunity.

        :param str title: Título de la evidencia.
        :param list files: Lista de diccionarios con las claves 'name' (nombre del archivo) y 'file' (contenido en base64).
        :param list signature_ids: ["una_firma_a_usar"].
        :return: Respuesta del API con los datos de la evidencia creada.
        :raises UserError: Si hay errores en los parámetros, conexión o respuesta del API.
        """
        if not title:
            raise UserError("El título es obligatorio para crear una evidencia.")
        if not files:
            raise UserError("Se requiere al menos un archivo para la evidencia.")
        if not signature_ids:
            raise UserError("Se requiere al menos un ID de firma para la evidencia.")

        url = f"{self._get_base_url()}/evidences"

        _logger.info("Creando evidencia en %s", url)
        payload = {
            "payload": {
                "title": title,
                "files": files,
            },
            "signatures": [{"id": sig_id} for sig_id in signature_ids],
        }

        _logger.info("Creando evidencia en %s", url)
        try:
            res = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
            )
            if res.status_code not in (200, 201):
                _logger.error("Error al crear evidencia: %s", res.text)
                raise UserError(f"Error creando evidencia ({res.status_code}): {res.text}")

            data = res.json().get('data') or res.json()
            return data

        except requests.exceptions.RequestException as e:
            _logger.error("Error de conexión al crear evidencia: %s", str(e))
            raise UserError(f"Error de conexión al crear evidencia: {str(e)}") from e