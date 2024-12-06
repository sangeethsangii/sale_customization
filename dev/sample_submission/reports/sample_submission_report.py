from odoo import models, api
from datetime import datetime

class SampleSubmissionReport(models.AbstractModel):
    _name = 'report.sample_submission.report_sample_submission'
    _description = 'Sample Submission Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sample.submission'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'sample.submission',
            'docs': docs,
            'data': data,
            'datetime': datetime,
        }
