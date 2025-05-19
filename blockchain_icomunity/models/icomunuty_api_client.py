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

    # @api.model
    # def create_signed_pdf(self, name, password, signature_id):
    #     """
    #     1) POST /signed_pdfs
    #        Body: { name (nombre del recurso, supongo deberia ir el de la factura),
    #        password (un pass que en algun momemto se pide, no lo se),
    #        signatures: [{id: signature_id}]  (los ids de las firmas con las que se quiere firmar, deberia ir el name de la firma que se crea con el proceso de KYC con el mail de Vicente }
    #        Devuelve data['ceryification']['links']['checker'] que es la url externa con la que consultar el estado (a menos que se use webhook)
    #     """
    #     url = f"{self._get_base_url()}/signed_pdfs"
    #     payload = {
    #         'name': name,
    #         'password': password,
    #         'signatures': [{'id': signature_id}],
    #     }
    #     _logger.info("Creando signed_pdf en %s", url)
    #     res = requests.post(url, json=payload, headers=self._get_headers(), timeout=10)
    #     if res.status_code not in (200, 201):
    #         _logger.error("Error al crear signed_pdf: %s", res.text)
    #         raise UserError(f"Error creando signed_pdf ({res.status_code}): {res.text}")
    #     data = res.json().get('data') or res.json()
    #     return data  # contiene 'id' y data['certification']['links']['checker']
    #
    # @api.model
    # def upload_pdfs(self, pdf_id, file_paths):
    #     """
    #     2) PUT /signed_pdfs/{id}/pdfs
    #        Adjunta el/los PDF(s) para firmar en blockchain, en el pdf creado anteriormente (osea, los pdf en ese pdf, basstante confuso)
    #     """
    #     base = self._get_base_url()
    #     url = f"{base}/signed_pdfs/{pdf_id}/pdfs"
    #     files_payload = []
    #     for path in file_paths:
    #         if not os.path.isfile(path):
    #             raise UserError(f"Archivo no encontrado: {path}")
    #         name = os.path.basename(path)
    #         files_payload.append(('files', (name, open(path, 'rb'), 'application/pdf')))
    #     _logger.info("Subiendo PDF a %s", url)
    #     res = requests.put(url, headers=self._get_headers(), files=files_payload, timeout=30)
    #
    #     for _, (_, fp, _) in files_payload:
    #         fp.close()
    #     if res.status_code not in (200, 201):
    #         _logger.error("Error al subir PDF: %s", res.text)
    #         raise UserError(f"Error subiendo PDF ({res.status_code}): {res.text}")
    #     return res.json()
    #
    # @api.model
    # def get_signed_pdf(self, pdf_id):
    #     """
    #     3) GET /signed_pdfs/{id}
    #        Devuelve detalle con blockchain info.
    #     """
    #     base = self._get_base_url()
    #     url = f"{base}/signed_pdfs/{pdf_id}"
    #     _logger.info("Consultando signed_pdf %s", pdf_id)
    #     res = requests.get(url, headers=self._get_headers(), timeout=10)
    #     if res.status_code != 200:
    #         _logger.error("Error al consultar signed_pdf: %s", res.text)
    #         raise UserError(f"Error fetching signed_pdf ({res.status_code}): {res.text}")
    #     return res.json().get('data') or res.json()  # incluye certification, hash, timestamp :contentReference[oaicite:4]{index=4}&#8203;:contentReference[oaicite:5]{index=5}


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
        print(f"URL: {url}")
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