{
    'name': 'Disable Delivery on Confirm',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Disables delivery on confirming SO and allows manual delivery creation',
    'depends': ['sale', 'stock'],
    'data': [
        'views/sale_order_view.xml',
        # 'views/stock_picking_view.xml',
        # 'data/disable_delivery_so.xml',
    ],
    'installable': True,
}

