from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    skip_delivery = fields.Boolean(
        string='Skip Delivery Creation',
        help='If checked, no delivery order will be created when confirming the sale',
        tracking=True
    )

    delivery_count = fields.Integer(
        string='Delivery Orders',
        compute='_compute_delivery_count',
        store=True
    )

    @api.depends('picking_ids')
    def _compute_delivery_count(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)

    def action_confirm(self):
        """Override to control delivery creation"""
        for order in self:
            # Store original auto_create_delivery value
            original_auto_create = order.env.company.stock_move_auto_assign

            if order.skip_delivery:
                # Temporarily disable auto delivery creation
                order.env.company.stock_move_auto_assign = False

            # Call standard confirmation
            res = super(SaleOrder, order).action_confirm()

            # Restore original setting
            order.env.company.stock_move_auto_assign = original_auto_create

        return res

    def action_create_delivery(self):
        """Create delivery order manually"""
        self.ensure_one()

        if self.state not in ['sale', 'done']:
            raise UserError(_('Cannot create delivery for draft/cancelled orders.'))

        if not self.order_line.filtered(lambda l: l.product_id.type in ['product', 'consu']):
            raise UserError(_('No storable products found to deliver.'))

        if self.picking_ids and any(p.state not in ['done', 'cancel'] for p in self.picking_ids):
            raise UserError(_('There are already ongoing deliveries for this order.'))

        return self._action_create_delivery_picking()

    def _action_create_delivery_picking(self):
        """Helper method to create delivery picking"""
        self.ensure_one()
        StockPicking = self.env['stock.picking']

        if not self.picking_ids or all(p.state in ['done', 'cancel'] for p in self.picking_ids):
            # Get picking type
            picking_type = self.warehouse_id.out_type_id

            # Create picking
            vals = {
                'partner_id': self.partner_shipping_id.id,
                'picking_type_id': picking_type.id,
                'origin': self.name,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': self.partner_shipping_id.property_stock_customer.id,
                'move_type': 'direct',
                'sale_id': self.id,
                'company_id': self.company_id.id,
                'scheduled_date': fields.Datetime.now(),
            }
            picking = StockPicking.create(vals)

            # Create move lines
            moves = []
            for line in self.order_line.filtered(lambda l: l.product_id.type in ['product', 'consu']):
                move_vals = {
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'picking_id': picking.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                    'sale_line_id': line.id,
                    'company_id': self.company_id.id,
                }
                moves.append((0, 0, move_vals))

            if moves:
                picking.write({'move_lines': moves})
                picking.action_confirm()
                picking.action_assign()

                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Delivery Order'),
                    'res_model': 'stock.picking',
                    'res_id': picking.id,
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {'create': False},
                }

        return True

    def action_view_delivery(self):
        """Smart button action to view deliveries"""
        self.ensure_one()
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        pickings = self.picking_ids

        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        return action



