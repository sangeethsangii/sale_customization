from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    auto_create_delivery = fields.Boolean(
        string='Auto-create Delivery Orders',
        default=True,
        help='Default setting for automatic delivery order creation'
    )