# -*- coding: utf-8 -*-

import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


# MODEL_TO_USE = 'account.move'
MODEL_TO_USE = 'hr.attendance'

class ICommunityLabsWebhook(http.Controller):
    @http.route(
        ['/icommunity/webhook',],
        type='json', auth='public', methods=['POST'], csrf=False
    )
    def event_responses(self, **kwargs):
        try:
            payload = request.httprequest.get_json(force=True)
        except Exception as e:
            _logger.error('Invalid JSON payload: %s', e)
            return {'status': 'error', 'message': 'Invalid JSON'}

        event = payload.get('event')
        data = payload.get('data', {})

        _logger.info('Received iCommunityLabs event %s: %s', event, data)

        evidence_id = data.get('evidence_id')
        status = event
        checker_url = data.get('checker_url')

        ActiveModel = request.env[MODEL_TO_USE].sudo()

        record = ActiveModel.search([('blockchain_evidence_id', '=', evidence_id)], limit=1)
        if not record:
            _logger.warning(f"No record found for evidence_id {evidence_id} in model {MODEL_TO_USE}")
            return {'status': 'error', 'message': 'Invoice not found'}

        record.write({
            'blockchain_status': status,
            'blockchain_webhook_data': pprint.pformat(payload, indent=4),
            'blockchain_checker_url': checker_url,
        })
        _logger.debug(f"Updated record {record.id} with status {status} and checker URL {checker_url}")

        return {'status': 'success'}

