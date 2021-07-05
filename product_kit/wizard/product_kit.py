# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductKit(models.TransientModel):
    _name = "product.kit"
    _description = "Kit Productos"

    product_kit_id = fields.Many2one('product.product', domain=[('is_kit', '=', True)], string="Product")
    quantity = fields.Integer('Quantity', default=1)
    sub_product_line_ids = fields.One2many('product.kit.lines', 'wizard_id', string="Sub Products")

    @api.onchange('product_kit_id')
    def get_sub_product_lines(self):
        sub_products = []
        for line in self.product_kit_id.sub_product_line_ids:
            line_id = self.env['product.kit.lines'].create({
                'wizard_id': self.id,
                'product_id': line.product_id.id,
                'quantity': self.quantity > 0 and line.quantity * self.quantity or line.quantity,
                'kit_qty': line.quantity,
                'qty_available': line.product_id.qty_available,
            })
            sub_products.append(line_id.id)
        self.update({'sub_product_line_ids': sub_products})

    @api.onchange('quantity')
    def change_quantity(self):
        if self.quantity > 0:
            for rec in self.sub_product_line_ids:
                rec.update({
                    'quantity': rec.kit_qty * self.quantity,
                })

    @api.multi
    def add_lines(self):
        self.ensure_one()
        if self.quantity <= 0:
            raise ValidationError(_('Kit Quantity must be grater than 0.'))
        if self._context.get('active_id'):
            sale_order_id = self.env['sale.order'].browse(self._context['active_id'])
            order_line = self.env['sale.order.line']
            for rec in self.sub_product_line_ids:
                vals = {
                    'order_id': sale_order_id.id,
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.quantity,
                    'product_kit_id': self.product_kit_id.id,
                }
                order_line = order_line.new(vals)
                order_line.product_id_change()
                order_line.create(vals)


class ProductKit_lines(models.TransientModel):
    _name = "product.kit.lines"
    _description = "Líneas Kit Productos"

    wizard_id = fields.Many2one('product.kit')
    product_id = fields.Many2one('product.product', domain=[('is_kit', '=', False)], string='Product')
    quantity = fields.Integer('Quantity', default=1)
    kit_qty = fields.Integer('Kit Quantity')
    qty_available = fields.Float('Available Quantity')

    @api.onchange('product_id')
    def get_available_qty(self):
        if self.product_id:
            self.update({
                'qty_available': self.product_id.qty_available,
            })

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
