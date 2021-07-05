# -*- coding: utf-8 -*-

from odoo import api, fields, models


class WebsiteProductCategory(models.Model):
    _inherit = 'product.public.category'
    
    description = fields.Html('Description for Category', translate=True)
    similares = fields.Boolean('Tener en cuenta para productos similares')
