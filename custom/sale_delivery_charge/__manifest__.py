{
    'name': 'Sale Delivery Charge',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Add a delivery charge field to Sale Orders',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
