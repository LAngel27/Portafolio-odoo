# -*- coding: utf-8 -*-
{
    'name': "POS Stock Product",

    'summary': """
        Show stock product POS""",

    'description': """
        Show stock product POS
    """,
    'author': "Consulnet",
    'website': "http://consulnet.cl",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'views/assets.xml',
        'views/pos_config_views.xml'
    ],
    'qweb': [
        'static/src/xml/Screens/ProductItem.xml',
        'static/src/xml/Screens/Orderline.xml',
        'static/src/xml/Screens/SetWarenhouseStockButton.xml',
        'static/src/xml/Popups/SelectorWarehouseModal.xml'
    ],
    'installable': True,
    'auto_install': False,
    'demo': [],
    'test': [],
}
