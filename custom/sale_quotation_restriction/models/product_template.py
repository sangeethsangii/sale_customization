from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_quotation_only_product = fields.Boolean(string='Quotation Only Product')
