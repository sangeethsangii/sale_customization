from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectChecklist(models.Model):
    _name = 'project.checklist'
    _description = 'Project Checklist'

    project_id = fields.Many2one('project.project', string='Project', required=True)
    checklist_lines = fields.One2many('project.checklist.line', 'checklist_id', string='Checklist Lines')
    date = fields.Date('Date')
    notes = fields.Text('Notes')

    @api.model
    def create(self, vals):
        # Create the checklist
        checklist = super(ProjectChecklist, self).create(vals)

        # Check if checklist_lines are already provided in vals
        if not vals.get('checklist_lines'):
            # Fetch checklist master items and create lines if not already present
            checklist_master_items = self.env['checklist.master'].search([])
            checklist_lines = [
                (0, 0, {'checklist_master_id': item.id})
                for item in checklist_master_items
            ]
            checklist.checklist_lines = checklist_lines  # Directly assign checklist lines

        return checklist


class ProjectChecklistLine(models.Model):
    _name = 'project.checklist.line'
    _description = 'Project Checklist Line'

    checklist_id = fields.Many2one('project.checklist', string='Checklist', required=True)
    checklist_master_id = fields.Many2one('checklist.master', string='Checklist Item', required=True)
    date = fields.Date('Date')
    is_done = fields.Boolean('Done')
    not_applicable = fields.Boolean('Not Applicable')
    notes = fields.Text('Notes')

    @api.onchange('is_done', 'not_applicable')
    def _onchange_status(self):
        if self.is_done and self.not_applicable:
            if self._origin.is_done:
                self.not_applicable = False
            else:
                self.is_done = False

    @api.constrains('is_done', 'not_applicable')
    def _check_status(self):
        for record in self:
            if record.is_done and record.not_applicable:
                raise ValidationError("An item cannot be both 'Done' and 'Not Applicable' at the same time.")


class ChecklistMaster(models.Model):
    _name = 'checklist.master'
    _description = 'Checklist Master'

    name = fields.Char(string='Checklist Name', required=True)


class Project(models.Model):
    _inherit = 'project.project'

    checklist_count = fields.Integer(
        string='Checklist Count',
        compute='_compute_checklist_count'
    )
    is_checklist = fields.Boolean('Is Checklist', default=True)

    def _compute_checklist_count(self):
        for project in self:
            project.checklist_count = self.env['project.checklist'].search_count([
                ('project_id', '=', project.id)
            ])

    def open_checklist_form(self):
        # Check if a checklist already exists for the project
        existing_checklist = self.env['project.checklist'].search([('project_id', '=', self.id)], limit=1)
        if not existing_checklist:
            # Create a new checklist only if one doesn't already exist
            existing_checklist = self.env['project.checklist'].create({
                'project_id': self.id,
                'date': fields.Date.today(),
            })

        return {
            'name': 'Project Checklist',
            'type': 'ir.actions.act_window',
            'res_model': 'project.checklist',
            'view_mode': 'form',
            'target': 'current',
            'res_id': existing_checklist.id,
            'views': [(False, 'form')],
        }
