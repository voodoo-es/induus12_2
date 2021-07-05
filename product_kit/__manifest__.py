# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'Product Kit',
    'version' : '1.1',
    'summary': 'Product can be sold as a Kit',
    'sequence': 30,
    'description': """
Product can be sold as a Kit.
    """,
    'category': 'Sales',
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'www.synconics.com',
    'depends': ['sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_kit_view.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [

    ],
    'images': [
        'static/description/main_screen.jpg'
    ],
    'price': 30.0,
    'currency': 'EUR',
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: