import logging

from odoo.addons.alan_customize.controllers.main import WebsiteSale
from odoo.addons.seo_url_redirect.models.ir_http import slug
from odoo.http import route, request

_logger = logging.getLogger(__name__)
PPG = 20

class WebsiteSale(WebsiteSale):

    @route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        result = super(WebsiteSale, self).shop(page=page, category=category, search=search, ppg=ppg, **post)
        qcontext = result.qcontext
        url = "/shop"

        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if category:
                url = "/shop/category/%s" % slug(category)

        if qcontext.get("search_count"):
            pager = request.website.pager(url=url, total=qcontext.get("search_count"), page=page, step=ppg, scope=7, url_args=post)
            result.qcontext.update(pager=pager)

        return result
