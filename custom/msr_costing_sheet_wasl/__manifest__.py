{
    "name": "MSR - Costing Sheet WASL",
    "description": """Costing Sheet WASL""",
    "website": "https://machinser.com",
    "summary": """Costing Sheet WASL""",
    "version": "17.0.1.0.0",
    "category": "Accounting",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "purchase",
        "account",
        "project",
        "mrp",
        "crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_template_data.xml",
        "data/ir_sequence_data.xml",
        "views/costing_sheet_views.xml",
        "views/product_views.xml",
        "views/product_components.xml",
        "views/crm_views.xml",
        'report/ir_actions_report_templates.xml',
        'report/ir_actions_report.xml',
    ],
}

