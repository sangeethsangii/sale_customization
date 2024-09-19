from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_charge = fields.Float(string='Delivery Charge', default=0.0)

    @api.depends('order_line.price_total', 'delivery_charge')
    def _compute_amount(self):
        for order in self:
            total = sum(line.price_total for line in order.order_line)
            order.amount_total = total + order.delivery_charge

