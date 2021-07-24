# -*- coding: utf-8 -*-
{
    'name': "account check payment",

    'summary': """
       Modulo creado para permitir la emision de cheque""",

    'description': """
        Modulo creado para permitir la emision de cheque
    """,

    'author': "Consulnet",
    'website': "http://consulnet.cl",
    'contribuitors': "LAngel Cartaya <correo>",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'report/report_invoice_with_payments_inh.xml',
        'views/account_payment_register_view.xml',
        'views/account_payment_view.xml',
    ],
}
