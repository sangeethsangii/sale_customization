from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    serial_number = fields.Char(string="Serial Number", readonly=True, copy=False)
    reverse_serial_number = fields.Char(string="Reverse Serial", readonly=True, copy=False)
    is_reversed = fields.Boolean(string="Is Reversed", default=False)

    @api.model
    def create(self, vals):
        # Generate initial serial number on quotation creation
        vals['serial_number'] = self.env['ir.sequence'].next_by_code('sale.order.serial') or '/'
        return super(SaleOrder, self).create(vals)

    def action_reverse(self):
        # Increment the revision number based on changes
        if self.serial_number and not self.is_reversed:
            base_serial = self.serial_number
            # Count previous revisions of the same serial number
            rev_count = self.env['sale.order'].search_count([
                ('serial_number', '=', base_serial),
                ('is_reversed', '=', True)
            ])
            new_serial = f"{base_serial} REV{rev_count + 1}"
            # Set reverse serial and mark current as reversed
            self.reverse_serial_number = new_serial
            self.is_reversed = True
            # Duplicate the sale order with updated serial number for the new revision
            new_order = self.copy()
            new_order.write({
                'serial_number': new_serial,
                'is_reversed': False  # Reset is_reversed for the new order
            })
            # Log the history
            self.message_post(body=f"Quotation reversed: new revision created {new_serial}")
        return new_order
