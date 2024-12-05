{
    'name': 'Custom Sales Filter',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom filters for sales quotations',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_filter_view.xml',
        'views/wizard_view.xml',
    ],
    'installable': True,
    'application': False,
}