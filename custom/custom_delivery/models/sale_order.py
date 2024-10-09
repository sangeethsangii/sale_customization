from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    create_delivery = fields.Boolean(
        string='Auto-create Delivery',
        default=lambda self: self.env.company.auto_create_delivery,
        help='If checked, delivery order will be created automatically upon sales order confirmation'
    )

    def action_confirm(self):
        original_auto_create = self.env.company.auto_create_delivery
        try:
            for order in self:
                self.env.company.auto_create_delivery = order.create_delivery
                super(SaleOrder, order).action_confirm()
        finally:
            self.env.company.auto_create_delivery = original_auto_create
        return True

    def action_create_delivery(self):
        self.ensure_one()
        if self.state not in ['sale', 'done']:
            raise UserError(_('Cannot create delivery order for draft/cancelled sales order.'))

        if not self.order_line.filtered(lambda l: l.product_id.type in ['product', 'consu']):
            raise UserError(_('No storable products found to deliver.'))

        if not self.picking_ids or all(p.state in ['done', 'cancel'] for p in self.picking_ids):
            return self._create_picking()

        raise UserError(_('There are already ongoing delivery orders for this sales order.'))
