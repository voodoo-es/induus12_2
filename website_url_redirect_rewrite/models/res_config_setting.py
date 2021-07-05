# -*- coding: utf-8 -*-
from odoo import api, models,fields


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'


    canonical_url = fields.Char(related='website_id.canonical_url',readonly=False)