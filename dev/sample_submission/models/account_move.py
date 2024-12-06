from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    sample_submission_id = fields.Many2one('sample.submission', string='Sample Submission', readonly=True)

    def action_view_sample_submission(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sample Submission',
            'res_model': 'sample.submission',
            'res_id': self.sample_submission_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
