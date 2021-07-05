# -*- coding: utf-8 -*-
from odoo import api, models,fields
from odoo.http import request
from urllib.parse import urlparse, urljoin
from odoo.addons.http_routing.models.ir_http import slug


class Website(models.Model):
    _inherit = "website"


    canonical_url = fields.Char(string="Canonical Url",help='Canonical domain is used to build unique canonical URLs '
             'to make SEO happy.')

    @api.multi
    def get_canonical_url(self, req=None):
        return urljoin(
            self._get_canonical_domain(),
            self._get_canonical_relative_url(req=req)
        )

    @api.multi
    def _get_canonical_domain(self):
        self.ensure_one()
        if self.canonical_url:
            return self.canonical_url
        params = self.env['ir.config_parameter'].sudo()
        return params.get_param('web.base.url')

    @api.multi
    def _get_canonical_relative_url(self, req=None):
        req = req or request
        url = req.httprequest.path.partition('?')
        url = url[0]
        search_origin = self.env['website.seo.redirection'].search([("origin","=",url)]) 
        for rec in search_origin:
            url = rec.destination
        lang_path = '/'
        if req.lang != req.website.default_lang_code:
            lang_path = '/%s/' % req.lang
            url = lang_path.rstrip('/') + url
        if self._is_root_page(req.httprequest.path):
            url = lang_path
        return url

    def _is_root_page(self, url):
        return (
            self.menu_id.child_id and
            self.menu_id.child_id[0].url == url
        )


    @api.multi
    def enumerate_pages(self, query_string=None):
        """Show redirected URLs in search results."""
        query = query_string or ""
        seo_redirections = list()
        redirection_records = self.env["website.seo.redirection"].search([
            "|", ("origin", "ilike", query),
            ("destination", "ilike", query),
        ])
        for record in redirection_records:
            for url in record.origin, record.destination:
                if url not in seo_redirections:
                    seo_redirections.append(url)
        # Give super() a website to work with
        # if not request.website_enabled:
        #     self.ensure_one()
        #     request.website = self
        # Yield super()'s pages
        for page in super(Website, self).enumerate_pages(query_string):
            try:
                seo_redirections.remove(page["loc"])
            except ValueError:
                pass
            yield page
        # Remove website if we were supposed to have none
        # if not request.website_enabled:
        #     request.website = None
        # Yield redirected pages not detected by super()
        for page in seo_redirections:
            yield {"loc": page}

class SeoMetadata(models.AbstractModel):
    _inherit = 'website.seo.metadata'


    def _default_website_meta(self):
        res = super(SeoMetadata,self)._default_website_meta()
        company = request.website.company_id.sudo()
        title = (request.website or company).name
        if 'name' in self:
            title = '%s | %s' % (self.name, title)
        if request.website.social_default_image:
            img = '/web/image/website/%s/social_default_image' % request.website.id
        else:
            img = '/web/image/res.company/%s/logo' % company.id
        full_url = request.httprequest.full_path.partition('?')
        full_url = full_url[0]
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = self.env['website.seo.redirection'].search([("origin","=",full_url)])
        for rec in url:
            full_url = rec.destination

        default_opengraph = {
            'og:type': 'website',
            'og:title': title,
            'og:site_name': company.name,
            'og:url': base_url+full_url,
            'og:image': img,
        }
        default_twitter = {
            'twitter:card': 'summary_large_image',
            'twitter:title': title,
            'twitter:image': img + '/300x300',
        }

        if company.social_twitter:
            default_twitter['twitter:site'] = "@%s" % company.social_twitter.split('/')[-1]

        return {
            'default_opengraph': default_opengraph,
            'default_twitter': default_twitter,
        }
        return res



class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'


    @api.multi
    def _compute_website_url(self):
        record = super(ProductTemplateInherit, self)._compute_website_url()
        for product in self:
            product.website_url = "/shop/product/%s" % slug(product)
            search_url = self.env['website.seo.redirection'].search([('origin','=',product.website_url)])
            if search_url.destination:
                product.website_url = search_url.destination
            else:
                product.website_url = "/shop/product/%s" % slug(product)
        return record


