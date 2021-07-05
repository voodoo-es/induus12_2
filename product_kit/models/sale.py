# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_kit_id = fields.Many2one('product.product', string="Product Kit")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
