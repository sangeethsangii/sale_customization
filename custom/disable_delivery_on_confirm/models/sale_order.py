from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if self.env.context.get('delivery_disabled'):
            res = super(SaleOrder, self).action_confirm()
            self.delivery_disabled = True
        else:
            self.state = 'sent'
            res = True
        return res

    delivery_disabled = fields.Boolean('Disable Delivery', default=False)

    # state = fields.Selection(selection_add=[('to_delivery','To Delivery')])

    def create_delivery(self):
        self.ensure_one()
        picking = self.env['stock.picking'].create({

            'sale_order_id': self.id,
            'partner_id': self.partner_id.id,
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
        })
        return {
            'name': 'Create Delivery',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'view_mode': 'form',
            'target': 'new',
        }
