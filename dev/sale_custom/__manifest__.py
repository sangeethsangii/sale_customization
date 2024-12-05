{
    'name': 'Custom Sales Filter',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom filter for quotations',
    'description': """
        This module adds a custom filter wizard for quotations based on:
        - Salesperson
        - Date range
    """,
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/quotation_filter_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
