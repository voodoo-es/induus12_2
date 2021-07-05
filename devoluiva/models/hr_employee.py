# -*- coding: utf-8 -*-
# © 2020 Ingetive - <info@ingetive.com>

import logging
import babel
import dateutil.parser

from odoo.addons.induus.models.induus_db import InduusDB
from odoo import models, fields, api, tools, _
from datetime import timedelta
from odoo.addons.induus.models import date_utils

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = 'hr.employee'

    devoluiva_id_customer = fields.Integer('ID Empleado (Devoluiva)')
    devoluiva_journal_id = fields.Many2one('account.journal', string="Diario")
