{
    'name': 'Sale Quotation Restriction',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Prevent conversion of quotations with quotation-only products',
    'depends': ['sale', 'product'],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}