from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('partially', 'Partially'), ('closed', 'Closed')])

    @api.model
    def action_partially(self):
        self.write({'state': 'partially'})

        print(self)

    @api.model
    def action_closed(self):
        self.write({'state': 'closed'})
