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


class Currency(models.Model):
    _inherit = 'res.currency'

    devoluiva_id_currency = fields.Integer('ID moneda (Devoluiva)')
