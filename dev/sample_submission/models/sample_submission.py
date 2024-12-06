from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SampleSubmission(models.Model):
    _name = 'sample.submission'
    _description = 'Sample Submission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence_number desc'

    active = fields.Boolean(default=True, tracking=True)
    sequence_number = fields.Char('Sample Number', readonly=True, default=lambda self: _('New'))
    name = fields.Char('Name of Sample', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    submission_date = fields.Date('Date of Submission', default=fields.Date.today, tracking=True)
    description = fields.Text('Description')
    price = fields.Monetary('Price', tracking=True)
    discount = fields.Float('Discount (%)', tracking=True)
    vat = fields.Float('VAT (%)', tracking=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('doing', 'Doing'),
        ('completed', 'Completed')
    ], string='Stage', default='pending', tracking=True)

    material_ids = fields.One2many('sample.material', 'submission_id', string='Materials Required')
    total_amount = fields.Monetary('Total Amount', compute='_compute_total_amount', store=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    # Invoice related fields
    invoice_id = fields.Many2one('account.move', string='Invoice', copy=False)
    invoice_status = fields.Selection([
        ('no', 'Not Invoiced'),
        ('invoiced', 'Invoiced')
    ], string='Invoice Status', default='no', tracking=True)
    collected_payment = fields.Monetary(related='invoice_id.amount_paid', string='Collected Payment')
    balance = fields.Monetary(compute='_compute_balance')

    # Statistics fields
    total_product_qty = fields.Float('Total Product Quantity', compute='_compute_product_stats', store=True)
    total_product_cost = fields.Monetary('Total Product Cost', compute='_compute_product_stats', store=True)
    profit = fields.Monetary('Profit', compute='_compute_profit', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence_number', _('New')) == _('New'):
                vals['sequence_number'] = self.env['ir.sequence'].next_by_code('sample.submission')
        return super().create(vals_list)

    @api.depends('price', 'discount', 'vat')
    def _compute_total_amount(self):
        for record in self:
            amount = record.price
            if record.discount:
                amount -= (amount * record.discount / 100)
            if record.vat:
                amount += (amount * record.vat / 100)
            record.total_amount = amount

    @api.depends('invoice_id.amount_paid', 'total_amount')
    def _compute_balance(self):
        for record in self:
            record.balance = record.total_amount - (record.collected_payment or 0.0)

    @api.depends('material_ids.quantity', 'material_ids.product_id')
    def _compute_product_stats(self):
        for record in self:
            record.total_product_qty = sum(record.material_ids.mapped('quantity'))
            record.total_product_cost = sum(line.product_id.standard_price * line.quantity
                                            for line in record.material_ids)

    @api.depends('total_amount', 'total_product_cost')
    def _compute_profit(self):
        for record in self:
            record.profit = record.total_amount - record.total_product_cost

    def action_create_invoice(self):
        self.ensure_one()
        if self.invoice_status == 'invoiced':
            raise UserError(_('Invoice already created for this submission.'))
        return {
            'name': _('Create Invoice?'),
            'type': 'ir.actions.act_window',
            'res_model': 'sample.submission.invoice.confirm',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_submission_id': self.id}
        }

    def _create_invoice(self):
        invoice_vals = {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_origin': self.sequence_number,
            'invoice_line_ids': [(0, 0, {
                'name': self.name,
                'price_unit': self.price,
                'quantity': 1,
                'discount': self.discount,
                'tax_ids': [(6, 0, self.env['account.tax'].search(
                    [('type_tax_use', '=', 'sale'), ('amount', '=', self.vat)]).ids)]
            })]
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.write({
            'invoice_id': invoice.id,
            'invoice_status': 'invoiced'
        })
        return invoice

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
