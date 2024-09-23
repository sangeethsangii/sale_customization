from odoo import models, fields, api
from odoo.exceptions import UserError

# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     @api.model
#     def create(self, vals):
#         order = super(SaleOrder, self).create(vals)
#         self._check_quotation_only_products(order)
#         return order
#
#     def action_confirm(self):
#         for order in self:
#             self._check_quotation_only_products(order)
#         return super(SaleOrder, self).action_confirm()
#
#     def _check_quotation_only_products(self, order):
#         for line in order.order_line:
#             if line.product_id.is_quotation_only_product:
#                 raise UserError("You cannot convert a quotation to a sales order because it contains quotation-only products.")
#
#

