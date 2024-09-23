from odoo import models, fields
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     # Define the new states in the state field
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('sent', 'Quotation Sent'),
#         ('sale', 'Sales Order'),
#         ('done', 'Locked'),
#         ('cancel', 'Cancelled'),
#         ('partially', 'Partially'),
#         ('closed', 'Closed'),
#     ], string='Status', readonly=True, index=True, copy=False, default='draft')
#
#     def action_partially(self):
#         self.ensure_one()
#         if self.state not in ['partially', 'closed']:
#             self.write({'state': 'partially'})
#
#     def action_closed(self):
#         self.ensure_one()
#         if self.state != 'closed':
#             self.write({'state': 'closed'})
