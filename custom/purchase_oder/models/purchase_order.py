from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    contract_number = fields.Char(string='Contract Number')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    contract_number = fields.Char(string='Contract Number', related='order_id.contract_number', store=True)
