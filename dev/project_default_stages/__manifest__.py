{
    'name': 'Project Default Stages',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Add default stages to new projects',
    'description': """
        Automatically adds predefined stages to newly created projects:
        - New
        - Assigned
        - In Progress
        - Done
    """,
    'author': '',
    'website': '',
    'depends': ['project'],
    'data': [
        'views/project_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
