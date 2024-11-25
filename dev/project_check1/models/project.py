from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'

    checklist_count = fields.Integer(compute='_compute_checklist_count', string='Checklist Count')
    checklist_ids = fields.One2many('project.checklist', 'project_id', string='Checklists')

    def _compute_checklist_count(self):
        for record in self:
            record.checklist_count = len(record.checklist_ids)

    def action_view_checklist(self):
        self.ensure_one()
        return {
            'name': 'Project Checklists',
            'type': 'ir.actions.act_window',
            'res_model': 'project.checklist',
            'view_mode': 'form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }
