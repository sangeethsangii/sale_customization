from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_create_delivery = fields.Boolean(
        related='company_id.auto_create_delivery',
        readonly=False,
        string='Auto-create Delivery Orders',
        help='If enabled, delivery orders will be created automatically when confirming sales orders'
    )