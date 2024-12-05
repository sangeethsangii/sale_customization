from odoo import api, fields, models

class QuotationFilterWizard(models.TransientModel):
    _name = 'quotation.filter.wizard'
    _description = 'Quotation Filter Wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    salesperson_id = fields.Many2one('res.users', string='Salesperson')

    def action_filter_quotations(self):
        domain = []
        if self.date_from:
            domain.append(('date_order', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_order', '<=', self.date_to))
        if self.salesperson_id:
            domain.append(('user_id', '=', self.salesperson_id.id))

        return {
            'name': 'Filtered Quotations',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'target': 'current',
        }
