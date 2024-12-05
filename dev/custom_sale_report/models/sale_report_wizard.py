from odoo import models, fields, api

class SaleReportWizard(models.TransientModel):
    _name = 'sale.report.wizard'
    _description = 'Sale Report Wizard'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)

    def generate_report(self):
        return self.env.ref('custom_sale_report.action_sale_custom_report').report_action(self)

    @api.model
    def generate_report_direct(self, sale_order_id):
        wizard = self.create({'sale_order_id': sale_order_id})
        return self.env.ref('custom_sale_report.action_sale_custom_report').report_action(wizard)

