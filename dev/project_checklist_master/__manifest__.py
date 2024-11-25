{
    'name': 'Project Checklist',
    'version': '1.0',
    'summary': 'Add checklists to projects',
    'description': """
        This module adds checklist functionality to projects.
        You can create and manage multiple checklist items for each project.
    """,
    'category': 'Project',
    'author': 'Your Name',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/checklist_master_views.xml',
        'views/checklist_master_menu.xml',
        'views/project_views.xml',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

