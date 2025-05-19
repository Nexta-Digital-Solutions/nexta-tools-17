# -*- coding: utf-8 -*-

import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

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

        AccountMove = request.env['account.move'].sudo()
        invoice = AccountMove.search([('blockchain_evidence_id', '=', evidence_id)], limit=1)
        if not invoice:
            _logger.warning('No invoice found for evidence ID %s', evidence_id)
            return {'status': 'error', 'message': 'Invoice not found'}

        invoice.write({
            'blockchain_status': status,
            'blockchain_webhook_data': pprint.pformat(payload, indent=4),
            'blockchain_checker_url': checker_url,
        })
        _logger.debug(f"Updated invoice {invoice.id} with status {status}")

        return {'status': 'success'}

