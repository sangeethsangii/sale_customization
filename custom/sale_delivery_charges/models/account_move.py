from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', )
    delivery_charge = fields.Float(string='Delivery Charge', )

    # @api.model
    # def create(self, vals):
    #     # Example logic to set sale_order_id if necessary
    #     if 'invoice_origin' in vals:
    #         sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
    #         if sale_order:
    #             vals['sale_order_id'] = sale_order.id
    #     return super(AccountMove, self).create(vals)





class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_delivery_charge = fields.Boolean(string="Is Delivery Charge" ,default=False)

