# -*- coding: utf-8 -*-
# © 2018 Ingetive - <info@ingetive.com>

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    print_zpl_ip = fields.Char("IP Impresora ZPL")
    print_zpl_port = fields.Integer("Puerto Impresora ZPL")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('print_zpl_ip', (self.print_zpl_ip or '').strip())
        set_param('print_zpl_port', (self.print_zpl_port or 0))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            print_zpl_ip=get_param('print_zpl_ip', default=''),
            print_zpl_port=int(get_param('print_zpl_port', default=0)),
        )
        return res
