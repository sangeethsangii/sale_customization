from odoo import models, fields, api

class ProjectChecklist(models.Model):
    _name = 'project.checklist'
    _description = 'Project Checklist'
    _rec_name = 'checklist_id'

    project_id = fields.Many2one('project.project', string='Project', required=True)
    checklist_id = fields.Many2one('checklist.master', string='Checklist', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    done = fields.Boolean(string='Done', default=False)
    not_applicable = fields.Boolean(string='Not Applicable', default=False)
    notes = fields.Text(string='Notes')
