from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    fixed_discount = fields.Float(string='Fixed Discount', digits='Product Price', default=0.0)

    @api.depends('product_uom_qty', 'price_unit', 'tax_id', 'discount')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)

            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.onchange('product_uom_qty', 'price_unit', 'discount')
    def _onchange_discount(self):
        self._compute_amount()

    @api.onchange('fixed_discount')
    def _onchange_fixed_discount(self):
        for line in self:
            if line.price_subtotal:
                line.discount = (line.fixed_discount / line.price_subtotal) * 100
            self._compute_amount()

    @api.onchange('discount')
    def _onchange_discount_update_fixed_discount(self):
        for line in self:
            if line.price_subtotal:
                line.fixed_discount = line.discount * line.price_subtotal / 100
            self._compute_amount()

    def _update_fixed_discount(self):
        for line in self:
            if line.price_subtotal:
                line.fixed_discount = line.discount * line.price_subtotal / 100


