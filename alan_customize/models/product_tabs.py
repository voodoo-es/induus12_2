# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTabHeads(models.Model):
    _name = 'product.tab_heads'
    _description = 'Product Tab heading'

    name = fields.Char(string='Tab Name', translate=True)
    active = fields.Boolean(string='Active', default=True)


class ProductTabSpecification(models.Model):
    _name = 'product.tabs'
    _order = 'tab_order, name'
    _description = 'Product Tab collection'

    name = fields.Many2one('product.tab_heads', string='Tab Name')
    active = fields.Boolean(string='Active', default=True)
    tab_content = fields.Html('Tab Content', sanitize=True, translate=True)
    tab_order = fields.Integer(string='Tab Order')
    product_tmpl_id = fields.Many2one('product.template', string="Product")


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    tab_ids = fields.One2many('product.tabs', 'product_tmpl_id', string='Product Tabs')
    similar_product_ids = fields.Many2many('product.template', 'product_similar_rel', 'src_id', 'dest_id',
                                           string='Productos similares', compute="_compute_similar_product_ids")


    def _compute_similar_product_ids(self):
        for r in self:
            categ_ids = []
            for categ in r.public_categ_ids:
                c = categ
                categ_hija_ids = []
                while c:
                    if c.similares:
                        categ_ids.append(c.id)
                        categ_ids += categ_hija_ids
                        break
                    elif c.parent_id:
                        categ_hija_ids.append(c.id)
                        c = c.parent_id
                    else:
                        c = None

            if categ_ids:
                products = self.env['product.template'].search([('public_categ_ids', 'in', categ_ids)])
                r.similar_product_ids = [(6, 0, [p.id for p in products])]
            else:
                r.similar_product_ids = None


