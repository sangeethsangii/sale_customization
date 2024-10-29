# from odoo import models, fields
#
#
# class SaleQuotationHistory(models.Model):
#     _name = 'sale.quotation.history'
#     _description = 'Sale Quotation Revision History'
#     _order = 'change_date desc'
#
#     sale_order_id = fields.Many2one(
#         'sale.order',
#         string='Sale Order',
#         required=True
#     )
#     old_quotation_number = fields.Char(
#         string='Old Quotation Number',
#         required=True
#     )
#     change_date = fields.Datetime(
#         string='Change Date',
#         required=True
#     )
