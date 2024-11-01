from odoo import models, fields, api
from odoo.tools.float_utils import float_is_zero


class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_due = fields.Monetary(
        string='Amount Due',
        compute='_compute_amount_due',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('state', 'line_ids', 'payment_state')
    def _compute_amount_due(self):
        for move in self:
            if move.state != 'posted' or move.payment_state == 'paid':
                move.amount_due = 0.0
            else:
                move.amount_due = move.amount_residual

