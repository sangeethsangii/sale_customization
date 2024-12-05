from odoo import models, fields, api

class SaleFilterWizard(models.TransientModel):
    _name = 'sale.filter.wizard'
    _description = 'Sales Filter Wizard'

    user_id = fields.Many2one('res.users', string='Salesperson')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def action_apply_filter(self):
        domain = []
        if self.user_id:
            domain.append(('user_id', '=', self.user_id.id))
        if self.date_from:
            domain.append(('date_order', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_order', '<=', self.date_to))

        return {
            'name': 'Filtered Quotations',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

