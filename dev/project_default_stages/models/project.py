from odoo import models, api, fields


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    is_default_stage = fields.Boolean(
        string='Default Stage',
        default=False,
        help="If checked, this stage will be automatically created for new projects"
    )
    default_sequence = fields.Integer(
        string='Default Sequence',
        default=10,
        help="Sequence number for default stages"
    )


class Project(models.Model):
    _inherit = 'project.project'

    @api.model_create_multi
    def create(self, vals_list):
        projects = super().create(vals_list)
        stage_obj = self.env['project.task.type']

        default_stages = stage_obj.search([
            ('is_default_stage', '=', True)
        ], order='default_sequence')

        if not default_stages:
            default_stages_data = [
                {'name': 'New', 'sequence': 1},
                {'name': 'Assigned', 'sequence': 2},
                {'name': 'In Progress', 'sequence': 3},
                {'name': 'Done', 'sequence': 4},
            ]

            for project in projects:
                for stage_data in default_stages_data:
                    stage_obj.create({
                        'name': stage_data['name'],
                        'sequence': stage_data['sequence'],
                        'project_ids': [(4, project.id)],
                    })
        else:
            for project in projects:
                for stage in default_stages:
                    stage_obj.create({
                        'name': stage.name,
                        'sequence': stage.default_sequence,
                        'project_ids': [(4, project.id)],
                    })

        return projects


