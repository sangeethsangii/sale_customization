from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_type = fields.Selection([
        ('material', 'Material'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('miscellaneous', 'Miscellaneous'),
        ('equipment_and_tools', 'Equipment & Tools'),
    ], string="Type")

