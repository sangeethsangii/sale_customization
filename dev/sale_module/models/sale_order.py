from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
