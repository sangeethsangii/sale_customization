{
    'name': 'Project Checklist1',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Add checklists to projects',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_checklist_views.xml',
        'views/checklist_master_views.xml',
        'views/project_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
