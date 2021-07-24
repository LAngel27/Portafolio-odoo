# -*- coding: utf-8 -*-
{
    'name': "Link payment",
    'summary': """Link payment""",
    'description': """link payment for invoices.""",
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'data/data_payment_icon.xml',
        'views/account_move_view.xml',
        'data/mail_template_data.xml',
        'data/mail_template_data_tasks.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
