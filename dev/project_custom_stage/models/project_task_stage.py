from odoo import fields, models, api


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    is_default_stage = fields.Boolean(string="Default Stage")


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
        default_stage_ids = self.env['project.task.type'].search([('is_default_stage', '=', True)])

        for project in projects:
            for default_stage_id in default_stage_ids:
                default_stage_id.project_ids += project
        return projects





