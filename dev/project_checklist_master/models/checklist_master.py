from odoo import models, fields, api


class ChecklistMaster(models.Model):
    _name = 'checklist.master'
    _description = 'Checklist '

    name = fields.Char(string='Name', required=True)



    project_id = fields.Many2one(
        'project.project',  # Related model
        string='Project',   # Label
        ondelete='cascade'  # Optional: Define behavior when the project is deleted
    )