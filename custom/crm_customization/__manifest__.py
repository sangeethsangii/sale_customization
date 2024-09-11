{
    'name': 'CRM Stage Restriction',
    'version': '1.0',
    'depends': ['crm'],
    'data': [
        'security/crm_security.xml',
        'views/crm_stage_views.xml',
        'models/crm_stage.py',
        'models/crm_lead.py',
    ],
    'installable': True,
    'application': False,
}