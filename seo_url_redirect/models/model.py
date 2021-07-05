from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
_log = logging.getLogger(__name__)


class Models(models.Model):

    _register = False

    @api.model
    def _add_magic_fields(self):
        super(Models, self)._add_magic_fields()
        self._add_field("url_key", fields.Char(
                            string='SEO Url Key',
                            default='',
                            translate=True,
                            help="SEO Url Key For Record"
                            )
                        )

    @api.multi
    def __check_url_key_uniq(self):
        for obj in self:
            if obj.url_key:
                urlKey = "/" + obj.url_key
                res = self.env['website.redirect'].sudo().search([('url_to', '=', urlKey), ('rewrite_val', '!=', 'custom')], 0, 2, 'id desc')
                if res:
                    for resObj in res:
                        if resObj.record_id == obj.id:
                            if resObj.rewrite_val != obj._name:
                                return False
                        else:
                            return False
        return True




    _constraints = [(__check_url_key_uniq, 'SEO URL Key must be unique for every Record!', ['url_key'])]
