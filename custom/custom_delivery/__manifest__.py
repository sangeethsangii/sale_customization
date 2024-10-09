{
    'name': 'Custom Delivery Control',
    'version': '17.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Control delivery creation from sales orders',
    'description': """
        This module allows:
        - Disabling automatic delivery creation when confirming sales orders
        - Adding a button to manually create delivery when needed
    """,
    'depends': ['sale_stock'],
    'data': [
        'views/sale_order_views.xml',
        # 'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
