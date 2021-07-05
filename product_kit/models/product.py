# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean('Use as Kit')
    sub_product_line_ids = fields.One2many('sub.product.lines', 'product_tmpl_ref_id', string='Sub Products')


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_kit = fields.Boolean('Use as Kit', related='product_tmpl_id.is_kit', store=True)


class SubProductLines(models.Model):
    _name = "sub.product.lines"
    _description = "Líneas Sub Productos"

    product_id = fields.Many2one('product.product', domain=[('is_kit', '=', False)], string='Product')
    product_tmpl_ref_id = fields.Many2one('product.template', string='Product Reference')
    quantity = fields.Integer('Quantity', default=1)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
