{
    'name': 'Custom Sale Report',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_report_wizard_view.xml',
        'reports/sale_report.xml',
        'reports/sale_report_template.xml',
    ],
    'installable': True,
    'application': False,
}