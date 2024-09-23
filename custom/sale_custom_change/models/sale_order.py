# from odoo import models, fields, api, exceptions
#
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     def action_confirm(self):
#         for order in self:
#             # Filter order lines with products marked as 'is_quotation_only_product'
#             quotation_lines = order.order_line.filtered(
#                 lambda line: line.product_id.is_quotation_only_product
#             )
#             if quotation_lines:
#                 raise exceptions.UserError(
#                     'You cannot confirm a quotation because it contains quotation only products.'
#                 )
#         return super(SaleOrder, self).action_confirm()
#
#
# class ProductProduct(models.Model):
#     _inherit = 'product.template'
#
#     is_quotation_only_product = fields.Boolean(
#         string='Quotation Only Product',
#         help='If checked, this product can only be used in quotations and cannot be sold.'
    )
