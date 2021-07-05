# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    product_kit_id = fields.Many2one('product.product', string='Product Kit', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['product_kit_id'] = ", l.product_kit_id as product_kit_id"
        groupby += ', l.product_kit_id'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: