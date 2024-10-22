from odoo import models, fields, api

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    _order = 'invoice_issue_date desc, invoice_number desc'

    # Vendor Details
    vendor_name = fields.Char(string="Vendor Name")
    vendor_street = fields.Char(string="Street Name")
    vendor_building = fields.Char(string="Building No")
    vendor_city = fields.Char(string="City")
    vendor_district = fields.Char(string="District")
    vendor_zip = fields.Char(string="Postal Code")
    vendor_country = fields.Char(string="Country")
    vendor_vat = fields.Char(string="VAT Number")
    vendor_crn = fields.Char(string="CRN")

    # Customer Details
    customer_name = fields.Char(string="Customer Name")
    customer_street = fields.Char(string="Customer Street Name")
    customer_building = fields.Char(string="Customer Building No")
    customer_city = fields.Char(string="Customer City")
    customer_district = fields.Char(string="Customer District")
    customer_zip = fields.Char(string="Customer Postal Code")
    customer_country = fields.Char(string="Customer Country")
    customer_vat = fields.Char(string="Customer VAT Number")
    customer_crn = fields.Char(string="Customer CRN")

    # Bank Details
    bank_name = fields.Char(string="Bank Name")
    account_name = fields.Char(string="A/C NAME")
    account_number = fields.Char(string="A/C NO")
    iban_number = fields.Char(string="IBAN NO")

    # Invoice Details
    invoice_number = fields.Char(string="Invoice No")
    invoice_issue_date = fields.Date(string="Invoice Issue Date")
    invoice_period_from = fields.Date(string="Invoice Period From")
    invoice_period_to = fields.Date(string="Invoice Period To")
    work_order_number = fields.Char(string="WO No")
    job_site = fields.Char(string="Job Site")
    remarks = fields.Text(string="Remarks")
    payment_terms = fields.Char(string="Payment Terms")
    vendor_number = fields.Char(string="Vendor No")
    contract_number = fields.Char(string="Contract No")
    ref_number = fields.Char(string="Ref No")
    po_number = fields.Char(string="PO No")

    # Financial Details
    total_excluding_vat = fields.Monetary(string="Total (Excluding VAT)", currency_field='company_currency_id')
    total_taxable_amount = fields.Monetary(string="Total Taxable Amount", currency_field='company_currency_id')
    total_vat_amount = fields.Monetary(string="Total VAT 15%", currency_field='company_currency_id')
    total_amount_due = fields.Monetary(string="Total Amount Due", currency_field='company_currency_id')

    # Service Details
    service_ref = fields.Char(string="Ref")
    service_unit = fields.Char(string="Unit")
    service_unit_price = fields.Monetary(string="Unit Price", currency_field='company_currency_id')
    service_quantity = fields.Float(string="Qty")
    service_total = fields.Monetary(string="Total", currency_field='company_currency_id')
    service_taxable_amount = fields.Monetary(string="Taxable Amount", currency_field='company_currency_id')
    service_tax_rate = fields.Float(string="Tax Rate")
    service_tax_amount = fields.Monetary(string="Tax", currency_field='company_currency_id')
    service_subtotal_inc_vat = fields.Monetary(string="Subtotal Inc Vat", currency_field='company_currency_id')




