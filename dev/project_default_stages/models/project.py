from odoo import models, fields, api
from odoo.tools.translate import _


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    _description = 'Project Task Stage'

    is_default_stage = fields.Boolean(
        string='Default Stage',
        default=False,
        help="If checked, this stage will be automatically created for new projects.",
        index=True,
    )
    default_sequence = fields.Integer(
        string='Default Sequence',
        default=10,
        help="Sequence number for default stages.",
    )

    @api.model
    def _get_default_stage_vals(self):
        """Define default stages configuration."""
        return [
            {
                'name': _('New x'),
                'sequence': 1,
                'fold': False,
                'is_default_stage': True,
            },
            {
                'name': _('Assigned x'),
                'sequence': 2,
                'fold': False,
                'is_default_stage': True,
            },
            {
                'name': _('In Progress x'),
                'sequence': 3,
                'fold': False,
                'is_default_stage': True,
            },
            {
                'name': _('Done x'),
                'sequence': 4,
                'fold': True,
                'is_default_stage': True,
            },
        ]


class Project(models.Model):
    _inherit = 'project.project'
    _description = 'Project'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to automatically create and assign default stages
        for new projects.
        """
        projects = super().create(vals_list)
        self._create_default_stages(projects)
        return projects

    def _create_default_stages(self, projects):
        """
        Create default stages for the given projects if they don't exist.

        Args:
            projects: recordset of projects
        """
        ProjectTaskType = self.env['project.task.type']
        default_stages = {}

        # Get or create default stages
        for stage_vals in ProjectTaskType._get_default_stage_vals():
            stage = ProjectTaskType.search([
                ('name', '=', stage_vals['name']),
                ('is_default_stage', '=', True)
            ], limit=1)

            if not stage:
                stage = ProjectTaskType.create(stage_vals)

            default_stages[stage_vals['name']] = stage

        # Assign stages to projects
        for project in projects:
            for stage in default_stages.values():
                if project.id not in stage.project_ids.ids:
                    stage.project_ids = [(4, project.id)]

    def copy(self, default=None):
        """
        Override copy method to ensure stages are properly copied
        when duplicating a project.
        """
        project = super().copy(default)
        self._create_default_stages(project)
        return project
