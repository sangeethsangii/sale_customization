{
    'name': 'Sale Delivery Control',
    'version': '17.0.1.0',
    'summary': 'Control delivery creation from sales orders',
    'description': """
        This module allows:
        - Disable automatic delivery creation when confirming sale orders
        - Add a new button to create delivery orders manually when needed

       
    """,
    'category': 'Sales',
    'author': 'Your Company',
    'website': '',
    'depends': [
        'sale_stock',
        'stock',
        'delivery',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
