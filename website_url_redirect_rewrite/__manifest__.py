# -*- coding: utf-8 -*-
{
    'name': """
Website URL Redirect URL Rewrite""",

    'summary': """
       SEO URL Redirect / Rewrite for 301, Blog, E-commerce website or any URL""",

    'description': """
       This module allows to set redirection or rewrite URL in odoo using Following Steps:
    """,
    'category': 'Website',
    'version': '12.0.1.0.0',

    'depends': ['base', 'website','website_sale','product'],

    # always loaded
    'data': [
       'security/ir.model.access.csv',
        'data/seo_data.xml',
        'views/website_template_view.xml',
        'views/website_canonical_template.xml',
        'views/website_view_inherit.xml',
        'views/assets.xml',
        'views/website_seo_redirection_view.xml',
        'views/product_inherit.xml',
    ],
    'demo': [
	   'demo/assets_demo.xml',
       'demo/website_seo_redirection.xml',
	],
    'price': 25.00,
    'currency': 'EUR',
    'support': ': business@aagaminfotech.com',
    'author': 'Aagam Infotech',
    'website': 'http://aagaminfotech.com',
    'installable': True,
    'license': 'AGPL-3',
    'external_dependencies': {'python': ['qrcode', 'pyotp']},
    'images': ['static/description/images/Banner-Img.png'],
}