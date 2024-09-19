from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_charge = fields.Float(string='Delivery Charge')


    # @api.depends('order_line.price_total', 'delivery_charge')
    # def _compute_amount(self):
    #     for order in self:
    #
    #         # Calculate the total amount including delivery charge
    #
    #         order.amount_untaxed = sum(line.price_subtotal for line in order.order_line)
    #         order.amount_tax = sum(
    #             line.tax_id.compute_all(line.price_subtotal)['total_included'] for line in order.order_line)
    #         order.amount_total = order.amount_untaxed + order.amount_tax + order.delivery_charge
    #
    # amount_untaxed = fields.Monetary(string='Untaxed Amount', compute='_compute_amount', store=True)
    # amount_tax = fields.Monetary(string='Taxes', compute='_compute_amount', store=True)
    # amount_total = fields.Monetary(string='Total', compute='_compute_amount', store=True)








