{
    'name': 'Custom CRM Extension',
    'version': '1.0',
    'depends': ['crm'],
    'data': [
        'security/crm_stage_security.xml',
        'security/ir.model.access.csv',
        'views/crm_stage_views.xml',
    ],
    'installable': True,
    'application': False,
}
