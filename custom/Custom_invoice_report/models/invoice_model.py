from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Invoice Details
    invoice_period_from = fields.Date(string='Invoice Period From')
    invoice_period_to = fields.Date(string='Invoice Period To')
    work_order_no = fields.Char(string='WO No')
    job_site = fields.Char(string='Job Site')
    remarks = fields.Text(string='Remarks')
    vendor_no = fields.Char(string='Vendor No')
    contract_no = fields.Char(string='Contract No')
    ref_no = fields.Char(string='Ref No')
    po_no = fields.Char(string='PO No')

    # Additional Address Fields
    partner_building_no = fields.Char(string='Building No')
    partner_additional_no = fields.Char(string='Additional No')
    partner_district = fields.Char(string='District')

    # Company Additional Fields
    company_building_no = fields.Char(string='Company Building No')
    company_additional_no = fields.Char(string='Company Additional No')
    company_district = fields.Char(string='Company District')

    # Amount in Words
    amount_total_words = fields.Char(compute='_compute_amount_words', string='Amount in Words')
    amount_total_words_ar = fields.Char(compute='_compute_amount_words', string='Amount in Words (Arabic)')

    @api.depends('amount_total')
    def _compute_amount_words(self):
        for record in self:
            record.amount_total_words = record.currency_id.amount_to_text(record.amount_total)
            # You would need to implement Arabic conversion separately
            record.amount_total_words_ar = record.currency_id.amount_to_text(record.amount_total)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    equipment_code = fields.Char(string='Equipment Code')
    service_nature = fields.Char(string='Nature of Service')
    unit_type = fields.Selection([
        ('DAY', 'Day'),
        ('TRIP', 'Trip'),
        # Add other unit types as needed
    ], string='Unit Type')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    building_no = fields.Char(string='Building No')
    additional_no = fields.Char(string='Additional No')
    district = fields.Char(string='District')
    vat_number = fields.Char(string='VAT Number')
    cr_number = fields.Char(string='CR Number')


class ResCompany(models.Model):
    _inherit = 'res.company'

    building_no = fields.Char(string='Building No')
    additional_no = fields.Char(string='Additional No')
    district = fields.Char(string='District')
    vat_number = fields.Char(string='VAT Number')
    cr_number = fields.Char(string='CR Number')
    bank_account_name = fields.Char(string='Bank Account Name')
    bank_account_number = fields.Char(string='Bank Account Number')
    bank_name = fields.Char(string='Bank Name')
    iban = fields.Char(string='IBAN')