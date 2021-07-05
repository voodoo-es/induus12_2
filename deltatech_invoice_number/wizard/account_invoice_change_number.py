# ©  2015-2019 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details


from odoo import api, fields, models


class AccountInvoiceChangeNumber(models.TransientModel):
    _name = "account.invoice.change.number"
    _description = "Account Invoice Change Number"

    internal_number = fields.Char(string="Invoice Number")

    @api.model
    def default_get(self, fields_list):
        defaults = super(AccountInvoiceChangeNumber, self).default_get(fields_list)
        active_id = self.env.context.get("active_id", False)
        if active_id:
            invoice = self.env["account.invoice"].browse(active_id)
            defaults["internal_number"] = invoice.move_name

        return defaults

    @api.multi
    def do_change_number(self):
        active_id = self.env.context.get("active_id", False)
        if active_id:
            invoice = self.env["account.invoice"].browse(active_id)
            values = {"move_name": self.internal_number}
            if invoice.number:
                values["number"] = self.internal_number
            invoice.write(values)
            if invoice.state == "open":
                invoice.action_number()
