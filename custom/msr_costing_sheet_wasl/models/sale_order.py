from odoo import models, fields

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    costing_sheet_id = fields.Many2one('cost.sheet', copy=False)


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    cost_sheet_line_id = fields.Many2one('cost.sheet.line', copy=False)