from odoo import models, fields
import base64
import xlsxwriter
from io import BytesIO
from datetime import datetime


class SampleSubmissionReportWizard(models.TransientModel):
    _name = 'sample.submission.report.wizard'
    _description = 'Sample Submission Report Wizard'

    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    report_type = fields.Selection([
        ('pdf', 'PDF Report'),
        ('excel', 'Excel Report')
    ], string='Report Type', default='pdf', required=True)

    excel_file = fields.Binary('Excel Report')
    excel_filename = fields.Char('Excel Filename')

    def action_generate_report(self):
        domain = [
            ('submission_date', '>=', self.date_from),
            ('submission_date', '<=', self.date_to)
        ]
        submissions = self.env['sample.submission'].search(domain)

        if self.report_type == 'pdf':
            return self.env.ref('sample_submission.action_report_sample_submission').report_action(submissions)
        else:
            return self._generate_excel_report(submissions)

    def _generate_excel_report(self, submissions):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Sample Submissions')

        # Formats
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#D3D3D3'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

        # Headers
        headers = ['Sample Number', 'Date', 'Customer', 'Amount', 'Status', 'Invoice Status']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Data
        for row, submission in enumerate(submissions, 1):
            worksheet.write(row, 0, submission.sequence_number)
            worksheet.write(row, 1, submission.submission_date, date_format)
            worksheet.write(row, 2, submission.partner_id.name)
            worksheet.write(row, 3, submission.total_amount)
            worksheet.write(row, 4, submission.state)
            worksheet.write(row, 5, submission.invoice_status)

        workbook.close()
        excel_data = output.getvalue()

        filename = f'Sample_Submissions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        self.write({
            'excel_file': base64.b64encode(excel_data),
            'excel_filename': filename
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model={self._name}&id={self.id}&field=excel_file&filename={filename}&download=true',
            'target': 'self',
        }
