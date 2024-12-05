from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    depend_task_id = fields.Many2one(
        'project.task',
        string="Depend Task",
        domain="[('id', '!=', id), ('project_id', '=', project_id)]"
    )

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id and self.depend_task_id:
            if self.depend_task_id.project_id != self.project_id:
                self.depend_task_id = False

    @api.onchange('depend_task_id')
    def _onchange_depend_task_id(self):
        if self.depend_task_id:
            if self.depend_task_id.stage_id.name != 'Done':

                self.depend_task_id = False
                return {
                    'warning': {
                        'title': 'Invalid Dependency',
                        'message': 'You can only select tasks that are in the Done stage as dependencies.'
                    }
                }


