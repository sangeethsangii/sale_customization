{
    'name': 'Custom Fields on Customer Invoice',
    'version': '1.0',
    'depends': ['base','account'],
    'data': [
        'security/my_custom_invoice_securtity.xml',
        # 'security/ir.model.access.csv',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
}