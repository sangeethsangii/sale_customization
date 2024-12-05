from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_filter_wizard(self):
        return {
            'name': 'Sales Filter Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.filter.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
