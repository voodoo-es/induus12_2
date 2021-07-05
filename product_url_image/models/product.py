# -*- encoding: utf-8 -*-

import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm
import base64  # file encode
from urllib.request import urlopen

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    image_url = fields.Char('Image URL')

    @api.model
    def create(self, vals):
        if vals.get('image_url'):
            try:
                vals['image'] = base64.encodestring(urlopen(vals.get('image_url')).read())
            except:
                pass
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('image_url'):
            try:
                vals['image'] = base64.encodestring(urlopen(vals.get('image_url')).read())
            except:
                pass
        return super(ProductTemplate, self).write(vals)


class ProductProduct(models.Model):
    _inherit = "product.product"

    image_url = fields.Char('Image URL')

    @api.model
    def create(self, vals):
        if vals.get('image_url'):
            try:
                vals['image'] = base64.encodestring(urlopen(vals.get('image_url')).read())
            except:
                pass
        return super(ProductProduct, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('image_url'):
            try:
                vals['image'] = base64.encodestring(urlopen(vals.get('image_url')).read())
            except:
                pass
        return super(ProductProduct, self).write(vals)

