from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    serial_number = fields.Char(string='Serial Number', readonly=True)
    is_reversed = fields.Boolean(string='Is Reversed', default=False)
    revision_number = fields.Integer(string='Revision Number', default=0)

    @api.model
    def create(self, vals):
        # Generate serial number for new sale order
        if vals.get('name', 'New') == 'New':
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('sale.order.serial')
        return super(SaleOrder, self).create(vals)

    def button_reverse(self):
        """
        Generate a new revision number and serial format each time reverse button is clicked,
        ensuring only one increment per click.
        """
        for order in self:
            # Increment revision number and generate new serial number
            order.revision_number += 1
            base_serial = order.serial_number.split(" REV")[0] if order.serial_number else ""
            new_serial = f"{base_serial} REV{order.revision_number}"

            # Update serial number and set is_reversed to True
            order.write({
                'is_reversed': True,
                'serial_number': new_serial
            })

    def action_confirm(self):
        # Maintain the serial number on initial confirmation
        if not self.serial_number:
            self.serial_number = self.env['ir.sequence'].next_by_code('sale.order.serial')
        return super(SaleOrder, self).action_confirm()

