from odoo import models, fields, api


# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     state = fields.Selection(selection_add=[
#         ('partially', 'Partially'),
#         ('closed', 'Closed')
#     ], ondelete={'partially': 'set default', 'closed': 'set default'})
#
#     @api.onchange('state')
#     def _onchange_state(self):
#         if self.state in ['partially', 'closed']:
#             for field in self._fields:
#                 if field not in ['state', 'name']:
#                     self[field] = self[field]
