# -*- coding: utf-8 -*-
# Copyright 2019 Adrián del Río <a.delrio@ingetive.com>

import logging
import requests
import json

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ImportarGastos(models.TransientModel):
    _name = 'devoluiva.importar_gastos'
    _description = 'Importar gastos'

    fecha_inicio = fields.Date('Fecha inicio', required=True, default=fields.Date.context_today)
    fecha_fin = fields.Date('Fecha fin', required=True, default=fields.Date.context_today)
    gasto_ids = fields.One2many('devoluiva.gastos_wizard', 'importar_gastos_id')

    def buscar_gastos_action(self):
        self.ensure_one()
        if not self.fecha_inicio or not self.fecha_fin:
            raise UserError("La fecha inicio y fin son obligatorias.")
        self.gasto_ids.unlink()

        pagina = 1
        total_paginas = 99
        while pagina <= total_paginas:
            url_gastos = "http://araniak.es/devoluiva/gastos.php?startDate=%s&endDate=%s&pageSize=%s" % \
                  (self.fecha_inicio.strftime("%Y-%m-%dT%H:%M:%S"), self.fecha_fin.strftime("%Y-%m-%dT%H:%M:%S"), pagina)
            response = requests.request("GET", url_gastos, headers={}, data={})
            data_gastos = json.loads(response.text)
            pagina = data_gastos['CurrentPage'] + 1
            total_paginas = data_gastos['TotalPages']

            monedas = {}

            for item in data_gastos['Items']:
                url_gasto = "http://araniak.es/devoluiva/gasto.php?id=%s" % item['Id']
                response = requests.request("GET", url_gasto, headers={}, data={})
                data_gasto = json.loads(response.text)

                if not data_gasto['Success']:
                    continue

                gasto_item = data_gasto['Result']

                product_tmpl = self.env['product.template'].search([
                    ('devoluiva_service_type', '=', item['ServiceType'])
                ], limit=1)

                employee = self.env['hr.employee'].search([
                    ('devoluiva_id_customer', '=', item['CustomerUser']['id'])
                ], limit=1)

                key_currency = str(item['CurrencyId'])
                currency_id = False
                if key_currency in monedas:
                    currency_id = monedas[key_currency]

                if not currency_id:
                    currency = self.env['res.currency'].search([
                        ('devoluiva_id_currency', '=', item['CurrencyId'])
                    ], limit=1)

                    if currency and currency.id not in monedas:
                        monedas.update({key_currency: currency.id})
                        currency_id = currency.id

                gasto = self.env['hr.expense'].search([('id_gasto_devoluiva', '=', item['Id'])], limit=1)

                tax_ids = []
                for t in gasto_item['TaxSummary']:
                    tax = self.env['account.tax'].search([
                        ('devoluiva_tax_type', '=', t['Type']),
                        ('devoluiva_tax_rate', '=', t['Rate'])
                    ], limit=1)
                    if tax:
                        tax_ids.append(tax.id)

                name = gasto_item['ServiceCustomTypeText']
                if 'name' in item['Store']:
                    name = "%s %s" % (name, item['Store']['name'])

                product_tmpl_id = False
                if product_tmpl:
                    product_tmpl_id = product_tmpl.id

                nif = False
                if 'supplierCompany' in item['Store'] and 'taxID' in item['Store']['supplierCompany']:
                    nif = item['Store']['supplierCompany']['taxID']

                partner_id = False
                if nif:
                    partner = self.env['res.partner'].search([('vat', '=', 'ES%s' % nif)], limit=1)
                    if partner:
                        partner_id = partner.id

                self.env['devoluiva.gastos_wizard'].create({
                    'importar_gastos_id': self.id,
                    'name': name,
                    'product_tmpl_id': product_tmpl_id,
                    'service_type': item['ServiceType'],
                    'subtotal': item['SubTotal'],
                    'total': item['Total'],
                    'number': item['Number'],
                    'issue_date': item['IssueDate'],
                    'name_customer_user': "%s %s" % (item['CustomerUser']['firstName'], item['CustomerUser']['lastName']),
                    'id_customer_user': item['CustomerUser']['id'],
                    'nif': nif,
                    'partner_id': partner_id,
                    'employee_id': employee.id if employee else None,
                    'id_currency': item['CurrencyId'],
                    'currency_id': currency_id,
                    'tax_ids': [(6, 0, tax_ids)] if tax_ids else None,
                    'id_gasto': item['Id'],
                    'existe': True if gasto else False,
                    'payment_mode': "company_account" if gasto_item['PaymentType'] == 'CompanyCard' else "own_account"
                })
        return self.open_wizard()

    def action_importar(self):
        self.ensure_one()
        for gasto in self.gasto_ids:
            if gasto.invalido or gasto.existe:
                continue

            journal_id = False
            if gasto.employee_id.devoluiva_journal_id:
                journal_id = gasto.employee_id.devoluiva_journal_id.id

            account_id = False
            if gasto.product_tmpl_id.property_account_expense_id:
                account_id = gasto.product_tmpl_id.property_account_expense_id.id

            expense = self.env['hr.expense'].create({
                'name': gasto.name,
                'product_id': gasto.product_tmpl_id.product_variant_id.id,
                'unit_amount': gasto.total,
                'reference': gasto.number,
                'id_gasto_devoluiva': gasto.id_gasto,
                'date': gasto.issue_date,
                'employee_id': gasto.employee_id.id,
                'account_id': account_id,
                'journal_id': journal_id,
                'partner_id': gasto.partner_id.id if gasto.partner_id else None,
                'currency_id': gasto.currency_id.id,
                'tax_ids': [(6, 0, gasto.tax_ids.ids)] if gasto.tax_ids else None,
                'payment_mode': gasto.payment_mode
            })

            url = "http://araniak.es/devoluiva/gasto_imagen.php?id=%s" % gasto.id_gasto
            response = requests.request("GET", url, headers={}, data={})
            data = json.loads(response.text)
            if data['Result']:
#                 self.env['documents.document'].create({
#                     'type': "binary",
#                     'name': "Gasto %s_%s" % (gasto.name, gasto.id_gasto),
#                     'res_model': 'hr.expense',
#                     'res_id': expense.id,
#                     'datas': data['Result']
#                 })
                
                self.env['ir.attachment'].create({
                    'type': "binary",
                    'name': "Gasto %s_%s" % (gasto.name, gasto.id_gasto),
                    'res_model': 'hr.expense',
                    'res_id': expense.id,
                    'datas': data['Result'],
                    'store_fname': 'Gasto - %s' % gasto.name,
                })

    @api.multi
    def open_wizard(self, context=None):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }


class GastosWizard(models.TransientModel):
    _name = 'devoluiva.gastos_wizard'
    _description = 'Gastos'
    _order = "issue_date desc"

    importar_gastos_id = fields.Many2one('devoluiva.importar_gastos', string="Importar Gastos", ondelete="cascade")
    existe = fields.Boolean("Existe")
    name = fields.Char('Nombre')
    service_type = fields.Integer('Tipo de servicio')
    product_tmpl_id = fields.Many2one('product.template', string="Producto")
    subtotal = fields.Monetary('Sub Total')
    total = fields.Monetary('Total')
    tax_ids = fields.Many2many('account.tax')
    number = fields.Char('Número')
    issue_date = fields.Datetime('Fecha')
    nif = fields.Char('NIF')
    partner_id = fields.Many2one('res.partner', string="Contacto")
    name_customer_user = fields.Char('Nombre empleado')
    id_customer_user = fields.Integer('ID Empleado')
    employee_id = fields.Many2one('hr.employee', ondelete="cascade")
    currency_id = fields.Many2one('res.currency', 'Currency', required=True)
    id_currency = fields.Integer('ID Moneda')
    id_gasto = fields.Integer('ID Gasto')
    invalido = fields.Boolean('Registro inválido', compute="_compute_invalido", store=True)
    payment_mode = fields.Selection([
        ("own_account", "Empleado (a reembolsar)"),
        ("company_account", "Compañia")
    ], default='own_account',string="Pagado por")

    @api.depends('product_tmpl_id', 'employee_id', 'currency_id')
    def _compute_invalido(self):
        for r in self:
            invalido = False
            if not r.product_tmpl_id or not r.employee_id or not r.currency_id:
                invalido = True
            r.invalido = invalido
