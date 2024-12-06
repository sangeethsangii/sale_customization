from odoo import models, fields, api


class SampleMaterial(models.Model):
    _name = 'sample.material'
    _description = 'Sample Material'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', default=10)
    submission_id = fields.Many2one('sample.submission', string='Sample Submission', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Material', required=True)
    quantity = fields.Float('Quantity', default=1.0)
    remarks = fields.Text('Remarks')
    company_id = fields.Many2one('res.company', related='submission_id.company_id', store=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    # Updated field definition to match the type of standard_price
    unit_cost = fields.Float('Unit Cost', related='product_id.standard_price', readonly=True)
    total_cost = fields.Monetary('Total Cost', compute='_compute_total_cost', store=True, currency_field='currency_id')

    @api.depends('quantity', 'unit_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * record.unit_cost
