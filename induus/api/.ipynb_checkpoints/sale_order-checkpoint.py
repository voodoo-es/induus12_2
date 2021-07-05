# -*- coding: utf-8 -*-
# © 2018 Ingetive - <info@ingetive.com>

import logging
import json

from odoo import http
from odoo.http import Controller, route, request

_logger = logging.getLogger(__name__)


class SaleOrderAPI(http.Controller):

    @http.route(['/api/v1/sale.order'], type='json', auth='api_key')
    def listado_sale_order(self, fecha_desde=None, fecha_hasta=None, offset=0, 
                           limit=10000, *args, **kwargs):
        domain=[]
        
        if fecha_desde:
            domain += [('date_order', '>=', fecha_desde)]
            
        if fecha_hasta:
            domain += [('date_order', '<=', fecha_hasta)]

        orders = request.env['sale.order'].sudo().search(domain, offset=offset, limit=limit)
        data = []
        for order in orders:
            data.append(self.get_values_order(order))
        return data
        
    def get_values_order(self, order):
        invoice = order.invoice_ids[0] if order.invoice_ids else None
        
        values = {
            'id': order.id,
            'fecha': order.date_order.strftime("%d/%m/%Y"),
            'pedido': order.name,
            'factura': invoice.number if invoice else '',
            'cliente': order.partner_id.name,
            'descripcion': order.note or '',
            'coste': order.coste,
            'portes': order.delivery_price or 0,
            'iva': order.amount_tax,
            'total_venta': order.amount_total,
            'beneficio': order.margin,
            'margen': order.margin_porcentaje,
            'forma_pago': order.payment_mode_id.name if order.payment_mode_id else '',
            'vencimiento': invoice.date_due if invoice else '',
            'importe_residual': invoice.residual if invoice else 0,
            'estado': invoice.state if invoice else '',
            'coste_analitico': 0,
            'beneficio_analitico':  order.margen_analitico
        }
        
        return values
        