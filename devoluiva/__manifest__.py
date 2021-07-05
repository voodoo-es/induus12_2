# -*- coding: utf-8 -*-
# © 2020 Ingetive - <info@ingetive.com>
{
    'name': "Devoluiva",
    'summary': """""",
    'author': "Ingetive",
    'website': "http://ingetive.com",
    'category': 'Uncategorized',
    'version': '12.0.1.0.1',
    'depends': [
        'base',
        'product',
        'hr_expense',
        'hr',
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/res_currency.xml',
        'views/hr_employee.xml',
        'views/hr_expense.xml',
        'views/account_tax.xml',
        'wizard/devoluiva_importar_gastos.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
