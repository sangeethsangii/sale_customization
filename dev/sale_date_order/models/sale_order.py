from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(
        string='Order Date',
        default=fields.Datetime.now,
        readonly=True, states={'draft': [('readonly', False)]}
    )

    @api.model
    def create(self, vals):
        # Set date_order to the current date and time if not provided when creating a new quotation
        if 'date_order' not in vals:
            vals['date_order'] = fields.Datetime.now()
        return super(SaleOrder, self).create(vals)

    def action_confirm(self):
        # Store the original date_order
        original_date = self.date_order

        # First call super to confirm the order
        result = super(SaleOrder, self).action_confirm()

        # Restore the original date_order if it was changed
        if self.date_order != original_date:
            self.write({'date_order': original_date})

        return result




