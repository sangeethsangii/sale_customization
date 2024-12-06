{
    'name': 'Sample Submission',
    'version': '17.0.1.0.0',
    'category': 'Services',
    'summary': 'Manage Sample Submissions and Materials',
    'description': """
        Sample Submission Management System
        Features:
        - Manage sample submissions
        - Track materials and requirements
        - Generate invoices
        - Export PDF and Excel reports
        - Material management wizard
        - Detailed statistics and analysis
    """,
    'author': 'Your Company',
    'website': '',
    'depends': [
        'base',
        'mail',
        'product',
        'account',

    ],
    'data': [
        'security/sample_submission_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizards/material_wizard_views.xml',
        'wizards/report_wizard_views.xml',
        'wizards/invoice_confirm_wizard_views.xml',
        'wizards/invoice_confirm_wizard_views.xml',
        'views/sample_submission_views.xml',
        'views/account_move_views.xml',
        'views/menu_views.xml',
        'reports/sample_submission_report.xml',
        'reports/sample_submission_templates.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'sample_submission/static/src/scss/report_styles.scss',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'sequence': 1,
}
