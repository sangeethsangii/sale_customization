from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    manager_remarks = fields.Char(string='Manager Remarks')
    director_remarks = fields.Char(string='Director Remarks')

    is_manager = fields.Boolean(string='Is Manager', compute='_compute_is_manager')
    is_director = fields.Boolean(string='Is Director', compute='_compute_is_manager')

    # Assuming user_id is related to the move
    @api.depends('is_manager', 'is_director')
    def _compute_is_manager(self):

        for record in self:
            user_id = self.env.user

            # print(user_id.has_group('my_custom_invoice.group_sales_custom_manager'))

            record.is_manager = user_id.has_group('my_custom_invoice.group_sales_custom_manager')
            record.is_director = user_id.has_group('my_custom_invoice.group_sales_custom_director')



    @api.onchange('state')
    def _onchange_state(self):
        if self.state != 'draft':
            self.manager_remarks = self.manager_remarks
            self.director_remarks = self.director_remarks


    @api.constrains('manager_remarks', 'director_remarks')
    def _check_remarks_fields(self):
        for invoice in self:
            if not invoice.manager_remarks or not invoice.director_remarks:
                raise ValidationError("Both Manager Remarks and Director Remarks must be filled before posting the invoice.")



