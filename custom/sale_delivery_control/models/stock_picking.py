from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sales Order',
        copy=False,
        readonly=True
    )

    @api.model
    def create(self, vals):
        """Override to handle custom picking creation"""
        picking = super(StockPicking, self).create(vals)

        # If created from sale order, link it
        if vals.get('origin'):
            sale_order = self.env['sale.order'].search([
                ('name', '=', vals['origin'])
            ], limit=1)
            if sale_order:
                picking.sale_id = sale_order.id

        return picking