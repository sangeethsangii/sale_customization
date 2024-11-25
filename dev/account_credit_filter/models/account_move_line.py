from odoo import models, fields, api
from ast import literal_eval

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _search_credit(self, operator, value):
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                value = 0.0
        return [('credit', operator, value)]

    @api.model
    def _search_debit(self, operator, value):
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                value = 0.0
        return [('debit', operator, value)]

