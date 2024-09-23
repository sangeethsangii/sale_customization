from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_charge = fields.Float(string="Delivery Charge", default=0.0)

    @api.onchange('delivery_charge')
    def _onchange_delivery_charge(self):
        for order in self:
            if order.delivery_charge:
                # Search for existing delivery charge line
                existing_line = order.order_line.filtered(lambda line: line.product_id.name == 'Delivery Charge')
                if existing_line:
                    # Update existing line if it already exists
                    existing_line.price_unit = order.delivery_charge  # Set price
                else:
                    # Create a new sale order line for delivery charge
                    product = self.env['product.product'].search([('name', '=', 'Delivery Charge')], limit=1)
                    if not product:
                        # Create the product if it doesn't exist
                        product = self.env['product.product'].create({
                            'name': 'Delivery Charge',
                            'type': 'service',  # Set as service type
                            'list_price': order.delivery_charge,
                        })
                    # Create the sale order line
                    self.env['sale.order.line'].create({
                        'order_id': order.ids[0],  # Ensure order_id is set correctly
                        'product_id': product.id,
                        'name': product.name,
                        'product_uom_qty': 1,
                        'price_unit': order.delivery_charge,
                    })
