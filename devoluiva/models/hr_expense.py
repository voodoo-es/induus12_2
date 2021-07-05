# -*- coding: utf-8 -*-
# © 2020 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api, tools, _

_logger = logging.getLogger(__name__)


class Expense(models.Model):
    _inherit = 'hr.expense'

    id_gasto_devoluiva = fields.Integer('ID gasto (Devoluiva)')
    journal_id = fields.Many2one('account.journal', string="Diario")
    partner_id = fields.Many2one('res.partner', string="Contacto")

    _sql_constraints = [
        ('unique_devoluiva', 'unique (id_gasto_devoluiva)', 'El ID gasto de devoluiva tiene que ser único.')
    ]

    @api.multi
    def action_submit_expenses(self):
        res = super(Expense, self).action_submit_expenses()
        todo = self.filtered(lambda x: x.payment_mode == 'own_account')

        journal_id = False
        if not todo:
            todo = []
            for r in self:
                if r.payment_mode == 'company_account' and not journal_id and r.journal_id:
                    journal_id = r.journal_id.id

                if r.journal_id and r.journal_id.id == journal_id:
                    todo.append(r)

        if not todo and not journal_id:
            self.filtered(lambda x: x.payment_mode == 'company_account')

        context = {'default_expense_line_ids': [t.id for t in todo]}
        if journal_id:
            context.update({'default_bank_journal_id': journal_id})

        res['context'].update(context)
        return res

    @api.multi
    def _get_account_move_line_values(self):
        move_line_values_by_expense = super(Expense, self)._get_account_move_line_values()
        for expense in self:
            move_line_values = move_line_values_by_expense.get(expense.id)
            for mlv in move_line_values:
                mlv.update({'partner_id': expense.partner_id.id if expense.partner_id else False})

        return move_line_values_by_expense
