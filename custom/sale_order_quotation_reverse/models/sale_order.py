# from odoo import models, fields, api
# from odoo.exceptions import UserError
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     quotation_number = fields.Char(
#         string='Quotation Number',
#         readonly=True,
#         copy=False
#     )
#     revision_count = fields.Integer(
#         string='Revision Count',
#         default=0,
#         copy=False
#     )
#     quotation_history_ids = fields.One2many(
#         'sale.quotation.history',
#         'sale_order_id',
#         string='Quotation History'
#     )
#
#     @api.model
#     def create(self, vals):
#         if not vals.get('quotation_number'):
#             vals['quotation_number'] = self.env['ir.sequence'].next_by_code('sale.quotation.number')
#         return super(SaleOrder, self).create(vals)
#
#     def action_reverse_quotation(self):
#         self.ensure_one()
#         if not self.quotation_number:
#             raise UserError('No quotation number found!')
#
#         # Create history record
#         self.env['sale.quotation.history'].create({
#             'sale_order_id': self.id,
#             'old_quotation_number': self.quotation_number,
#             'change_date': fields.Datetime.now(),
#         })
#
#         # Update revision count and generate new quotation number
#         self.revision_count += 1
#         self.quotation_number = f"{self.quotation_number}-REV{self.revision_count}"
#
#         return True