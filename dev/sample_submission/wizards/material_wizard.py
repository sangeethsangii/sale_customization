from odoo import models, fields, api

class MaterialWizard(models.TransientModel):
    _name = 'material.wizard'
    _description = 'Material Entry Wizard'

    submission_id = fields.Many2one('sample.submission', string='Sample Submission')
    material_line_ids = fields.One2many('material.wizard.line', 'wizard_id', string='Materials')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self._context.get('active_id'):
            res['submission_id'] = self._context.get('active_id')
        return res

    def action_confirm(self):
        for line in self.material_line_ids:
            self.env['sample.material'].create({
                'submission_id': self.submission_id.id,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'remarks': line.remarks,
            })
        return {'type': 'ir.actions.act_window_close'}

class MaterialWizardLine(models.TransientModel):
    _name = 'material.wizard.line'
    _description = 'Material Wizard Line'

    wizard_id = fields.Many2one('material.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Material', required=True)
    quantity = fields.Float('Quantity', default=1.0)
    remarks = fields.Text('Remarks')
