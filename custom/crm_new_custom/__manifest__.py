{
    'name': 'CRM Stage Restriction',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Add restriction for CRM stages',
    'depends': ['crm'],
    'data': [
        'views/crm_stage_views.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
}