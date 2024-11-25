from odoo import models, fields, api


class ChecklistMaster(models.Model):
    _name = 'checklist.master'
    _description = 'Checklist '

    name = fields.Char(string='Name', required=True)



