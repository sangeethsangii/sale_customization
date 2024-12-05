{
    'name': 'Custom Sales Filter',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom filters for quotations',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard_r/quotation_filter_view.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
