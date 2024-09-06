{
    'name': 'Sale Custom_change',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Customizations for sales orders',
    'description': 'Adds a field to mark products as quotation only and prevents conversion if such products are present.',
    'depends': ['sale', 'product'],
    'data': [
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
}
