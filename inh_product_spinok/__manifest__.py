{
    'name': 'Modificacion de producto',
    'category': 'stock',
    'depends': ['product', 'contacts', 'account'],
    'data': [
       'views/product_template_view.xml',
       'views/res_partner_view.xml'
    ],
    'installable': True,
    'application': True,
}