from odoo import models, fields

class SampleSubmissionInvoiceConfirm(models.TransientModel):
    _name = 'sample.submission.invoice.confirm'
    _description = 'Sample Submission Invoice Confirmation'

    submission_id = fields.Many2one('sample.submission', string='Sample Submission')

    def action_confirm(self):
        invoice = self.submission_id._create_invoice()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
