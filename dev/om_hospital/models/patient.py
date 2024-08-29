from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = "mail.thread"
    _description = "Patient records"

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    is_child = fields.Boolean(string='Is child ?', tracking=True)
    note = fields.Text(string='Notes')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string='Gender',
                              tracking=True)

    @api.onchange('age')
    def _onchange_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False
