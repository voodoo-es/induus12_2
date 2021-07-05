##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions, _
import calendar

_logger = logging.getLogger(__name__)


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    @api.one
    def compute(self, value, date_ref=False):
        """This method can't be new API due to arguments names are not
        standard for the API wrapper.
        """
        result = super(AccountPaymentTerm, self).compute(value=value, date_ref=date_ref)
        if not result or not result[0] or not result[0][0]:
            return []
        for i, line in enumerate(self.line_ids):
            if not line.payment_days:
                continue

            payment_days = line._decode_payment_days(line.payment_days)
            if not payment_days:
                continue

            new_date = None

            date = fields.Date.from_string(result[0][i][0])
            days_in_month = calendar.monthrange(date.year, date.month)[1]

            for day in payment_days:
                if day['range']:
                    range_day = day['range'].split("_")
                    date_order = date + relativedelta(days=1)
                    day_date = date_order.day
                    if day_date >= int(range_day[0]) and day_date <= int(range_day[1]):
                        new_date = date_order + relativedelta(day=day['day'])
                else:
                    if date.day <= day['day']:
                        if day['day'] > days_in_month:
                            day['day'] = days_in_month
                        new_date = date + relativedelta(day=day['day'])
                        break

            if not new_date:
                day = payment_days[0]['day']
                if day > days_in_month:
                    day = days_in_month
                new_date = date + relativedelta(day=day, months=1)
            result[0][i] = (fields.Date.to_string(new_date), result[0][i][1])

        return result[0]


class AccountPaymentTermLine(models.Model):
    _inherit = "account.payment.term.line"

    def _decode_payment_days(self, days_char):
        # Admit space, dash and comma as separators
        days_char = days_char.replace(' ', '-').replace(',', '-')
        days_char = [x.strip() for x in days_char.split('-') if x]
        days = []
        for day_c in days_char:
            if day_c.find('/') == -1:
                days.append({'day': int(day_c), 'range': ''})
            else:
                dc = day_c.split("/")
                range = ''
                if dc[1].find("_"):
                    range = dc[1]
                days.append({'day': int(dc[0]), 'range': range})

        days = sorted(days, key=lambda k: k['day'])
        return days

    @api.multi
    @api.constrains('payment_days')
    def _check_payment_days(self):
        for r in self:
            if not r.payment_days:
                return
            try:
                payment_days = r._decode_payment_days(r.payment_days)
                error = any(day['day'] <= 0 or day['day'] > 31 for day in payment_days)
            except:
                error = True
            if error:
                raise exceptions.Warning(
                    _('Payment days field format is not valid.'))

    payment_days = fields.Char(
        string='Payment day(s)',
        help="Put here the day or days when the partner makes the payment. "
             "Separate each possible payment day with dashes (-), commas (,) "
             "or spaces ( ).")
