# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_terms_of_service = fields.Boolean("Show Terms of Service on Sign up")
    enable_privacy_policy = fields.Boolean("Show Privacy Policy on Sign up")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        enable_terms_of_service = params.get_param('enable_terms_of_service', default=False)
        enable_privacy_policy = params.get_param('enable_privacy_policy', default=False)

        res.update(
            enable_terms_of_service=enable_terms_of_service,
            enable_privacy_policy=enable_privacy_policy)
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('enable_terms_of_service', self.enable_terms_of_service)
        self.env['ir.config_parameter'].set_param('enable_privacy_policy', self.enable_privacy_policy)
