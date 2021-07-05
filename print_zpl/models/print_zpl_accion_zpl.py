# -*- coding: utf-8 -*-
# © 2018 Ingetive - <info@ingetive.com>

import logging
import socket

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AccionZPL(models.AbstractModel):
    _name = 'print_zpl.accion_zpl'
    _description = 'Accion ZPL'

    def printZPL(self, records, texto_zpl):
        TCP_IP = self.env['ir.config_parameter'].sudo().get_param('print_zpl_ip', '')
        TCP_PORT = int(self.env['ir.config_parameter'].sudo().get_param('print_zpl_port', 0))

        if not TCP_IP:
            return

        for r in records:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                s.send(str(eval(texto_zpl)).encode())
                s.close()
            except Exception as e:
                _logger.error(e)
                pass

