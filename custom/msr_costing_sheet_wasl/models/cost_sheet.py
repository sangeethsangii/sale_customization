from odoo import fields, models, api, _

COST_SHEET_STATE = [
    ('draft', "Draft"),
    ('sent', "Sent"),
    ('confirm', "Confirmed"),
    ('approved', "Approved"),
    # ('quote_created', "Quotation Created"),
    ('cancel', "Cancelled"),
]


class CostSheet(models.Model):
    _name = "cost.sheet"
    _description = "Costing Sheet"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Name",
        required=True, copy=False, readonly=False,
        default=lambda self: _('New'))
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, change_default=True, index=True,
        tracking=1,
        domain="[('company_id', 'in', (False, company_id))]")
    state = fields.Selection(
        selection=COST_SHEET_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    client_order_ref = fields.Char(string="Customer Reference", copy=False)
    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Terms",
        compute='_compute_payment_term_id',
        store=True, readonly=False, precompute=True, check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string="Pricelist",
        compute='_compute_pricelist_id',
        store=True, readonly=False, precompute=True, check_company=True,
        tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected.")
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_currency_id',
        store=True,
        precompute=True,
        ondelete='restrict')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
            self.env.ref("sales_team.group_sale_salesman").id))
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string="Analytic Account",
        copy=False, check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    date_order = fields.Datetime(
        string="Date",
        required=True, copy=False,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.",
        default=fields.Datetime.now)
    project_id = fields.Many2one('project.project', string="Project")
    cost_line_ids = fields.One2many('cost.sheet.line', 'sheet_id', string="Cost Line")
    amount_before_margin = fields.Monetary(string="Total Cost Without VAT", store=True, compute='_compute_total_amount')
    amount_untaxed = fields.Monetary(string="Untaxed Amount", store=True, compute='_compute_total_amount')
    amount_tax = fields.Monetary(string="Tax", store=True, compute='_compute_total_amount')
    amount_total = fields.Monetary(string="Total", store=True, compute='_compute_total_amount')
    validity_date = fields.Date(
        string="Expiration Date")
    amount_margin = fields.Monetary(string="Margin", store=True, compute='_compute_total_amount')
    amount_contigency = fields.Monetary(string="Contigency", store=True, compute='_compute_total_amount')
    opportunity_id = fields.Many2one(
        'crm.lead', string='Opportunity', check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.depends('partner_id', 'company_id')
    def _compute_pricelist_id(self):
        for order in self:
            if order.state != 'draft':
                continue
            if not order.partner_id:
                order.pricelist_id = False
                continue
            order = order.with_company(order.company_id)
            order.pricelist_id = order.partner_id.property_product_pricelist

    @api.depends('partner_id')
    def _compute_payment_term_id(self):
        for order in self:
            order = order.with_company(order.company_id)
            order.payment_term_id = order.partner_id.property_payment_term_id

    @api.depends('pricelist_id', 'company_id')
    def _compute_currency_id(self):
        for order in self:
            order.currency_id = order.pricelist_id.currency_id or order.company_id.currency_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('name', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_order'])
                ) if 'date_order' in vals else None
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'cost.sheet', sequence_date=seq_date) or _("New")
        return super(CostSheet, self).create(vals_list)

    @api.depends('partner_id')
    def _compute_user_id(self):
        for order in self:
            if order.partner_id and not (order.user_id):
                order.user_id = (
                        order.partner_id.user_id
                        or order.partner_id.commercial_partner_id.user_id
                        or (self.user_has_groups('sales_team.group_sale_salesman') and self.env.user)
                )

    @api.depends('cost_line_ids.price_subtotal', 'cost_line_ids.margin_rate')
    def _compute_total_amount(self):
        for order in self:
            price_subtotal = 0.0
            price_total = 0.0
            amount_before_margin = 0.0
            margin_rate = 0.0
            contigency_rate = 0.0
            for line in order.cost_line_ids:
                price_subtotal = price_subtotal + line.price_subtotal
                price_total = price_total + line.price_total
                amount_before_margin = amount_before_margin + (line.product_uom_qty * line.price_unit)
                if line.margin_percentage:
                    margin_rate = margin_rate + (line.price_unit * (line.margin_percentage / 100))
                if line.margin_fixed:
                    margin_rate = margin_rate + line.margin_fixed
                if line.contigency_perc:
                    contigency_rate = contigency_rate + (line.price_unit * (line.contigency_perc / 100))

            price_tax = price_total - price_subtotal
            order.amount_untaxed = price_subtotal
            order.amount_total = price_total
            order.amount_tax = price_tax
            order.amount_margin = margin_rate
            order.amount_before_margin = amount_before_margin
            order.amount_contigency = contigency_rate

    def action_estimation_send(self):
        self.ensure_one()
        template_id = self.env.ref('msr_costing_sheet_wasl.email_template_estimation').id
        ctx = {
            'default_model': 'cost.sheet',
            'default_res_ids': [self.id],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            # 'mark_so_as_sent': True,  # Optional: Mark as sent
            'custom_layout': "mail.mail_notification_paynow",  # Optional: Custom email layout
        }
        self.write({'state': 'sent'})
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_create_quotation(self):
        ctx = dict(self.env.context)
        sale_vals = {
            'partner_id': self.partner_id.id,
            'opportunity_id': self.opportunity_id.id,
            'costing_sheet_id': self.id,
            'payment_term_id': self.payment_term_id.id,
            'pricelist_id': self.pricelist_id.id,
            'client_order_ref': self.client_order_ref,
            'project_id': self.project_id.id,
            'analytic_account_id': self.analytic_account_id.id
        }
        sale_id = self.env['sale.order'].create(sale_vals)
        for line in self.cost_line_ids:
            sale_line_vals = {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'tax_id': line.tax_ids.ids,
                'price_unit': line.margin_rate,
                'order_id': sale_id.id,
                'cost_sheet_line_id': line.id,
            }
            sale_line_id = self.env['sale.order.line'].create(sale_line_vals)
        return {
            "name": "Quotation",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": sale_id.id,
            "context": ctx,
            "target": "current",
        }


class CostSheetLine(models.Model):
    _name = "cost.sheet.line"
    _description = "Costing Sheet Line"

    sheet_id = fields.Many2one(
        comodel_name='cost.sheet',
        string="Order Reference",
        required=True, ondelete='cascade', index=True, copy=False)
    sequence = fields.Integer(string="Sequence", default=10)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        domain=[('product_type', 'not in', ('material', 'labour', 'overhead', 'miscellaneous'))],
        change_default=True, ondelete='restrict', index=True)
    name = fields.Text(
        string="Description", required=True)
    product_uom_qty = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure', default=1.0, required=True)
    product_uom = fields.Many2one(
        comodel_name='uom.uom', domain="[('category_id', '=', product_uom_category_id)]",
        string="Unit of Measure", ondelete='restrict')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    price_unit = fields.Float(
        string="Unit Price",
        digits='Product Price', required=True)
    discount = fields.Float(
        string="Discount (%)",
        digits='Discount',
        readonly=False)
    margin_percentage = fields.Float(string="Margin %", digits='Discount')
    margin_fixed = fields.Float(
        string="Margin (Fixed)",
        digits="Product Price"
    )
    margin_rate = fields.Float(string="Rate", compute='_compute_margin_amount',
                               store=True)
    contigency_perc = fields.Float(
        string="Contigency(%)",
        digits="Discount"
    )
    company_id = fields.Many2one(
        related='sheet_id.company_id',
        store=True, index=True)
    currency_id = fields.Many2one(
        related='sheet_id.currency_id',
        store=True)
    tax_ids = fields.Many2many(
        comodel_name='account.tax',
        string="Taxes")
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True)
    price_total = fields.Monetary(
        string="Total",
        compute='_compute_amount',
        store=True)
    price_tax = fields.Float(
        string="Total Tax",
        compute='_compute_amount',
        store=True, precompute=True)
    subproduct_line_id = fields.Many2one('product.components',
                                         string='Subproducts'
                                         )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.subproduct_line_id:
            self.subproduct_line_id = self.env['product.components'].search(
                [('product_id', '=', self.product_id.id), ('cost_sheet_line_id', '=', self.id)], limit=1).id
        self.price_unit = self.subproduct_line_id.amount_total
        self.name = self.product_id.name
        self.tax_ids = self.product_id.taxes_id
        self.product_uom = self.product_id.uom_id.id

    @api.depends('margin_percentage', 'margin_fixed', 'price_unit', 'contigency_perc')
    def _compute_margin_amount(self):
        for line in self:
            if line.price_unit:
                if line.margin_percentage:
                    if line.contigency_perc:
                        rate = line.price_unit + (line.price_unit * (line.margin_percentage / 100)) + (
                                line.price_unit * (line.contigency_perc / 100))
                        line.margin_rate = rate

                    else:
                        rate = line.price_unit + (line.price_unit * (line.margin_percentage / 100))
                        line.margin_rate = rate
                elif line.margin_fixed:
                    if line.contigency_perc:
                        rate = line.price_unit + line.margin_fixed + (line.price_unit * (line.contigency_perc / 100))
                        line.margin_rate = rate
                    else:
                        rate = line.price_unit + line.margin_fixed
                        line.margin_rate = rate
                else:
                    if line.contigency_perc:
                        line.margin_rate = line.price_unit + (line.price_unit * (line.contigency_perc / 100))
                    else:

                        line.margin_rate = line.price_unit

    def action_button_product_components(self):
        self.ensure_one()
        if self.product_id:
            components = self.subproduct_line_id if self.subproduct_line_id else self.env['product.components'].search(
                [('product_id', '=', self.product_id.id), ('cost_sheet_line_id', '=', self.id)], limit=1)
            if not components:
                bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)],
                                                 limit=1)
                component_vals = {
                    'product_id': self.product_id.id,
                    'cost_sheet_line_id': self.id,
                    'bom_id': bom.id if bom else False,
                }
                prd_components = self.env['product.components'].create(component_vals)
                if bom:
                    bom_line = bom.bom_line_ids
                    material_array = []
                    labour_array = []
                    overhead_array = []
                    miscellaneous_array = []
                    equipment_and_tools_array = []
                    for component in bom_line:
                        if component.product_id.product_type == 'material':
                            material_dict = {
                                'product_id': component.product_id.id,
                                'name': component.product_id.name,
                                'product_type': 'material',
                                'product_uom': component.product_uom_id.id,
                                'product_uom_qty': component.product_qty,
                                'price_unit': component.product_id.lst_price,
                            }
                            material_array.append((0, 0, material_dict))

                        if component.product_id.product_type == 'labour':
                            labour_dict = {
                                'product_id': component.product_id.id,
                                'name': component.product_id.name,
                                'product_type': 'labour',
                                'product_uom': component.product_uom_id.id,
                                'product_uom_qty': component.product_qty,
                                'price_unit': component.product_id.lst_price,
                            }
                            labour_array.append((0, 0, labour_dict))
                        if component.product_id.product_type == 'overhead':
                            overhead_dict = {
                                'product_id': component.product_id.id,
                                'name': component.product_id.name,
                                'product_type': 'overhead',
                                'product_uom': component.product_uom_id.id,
                                'product_uom_qty': component.product_qty,
                                'price_unit': component.product_id.lst_price,
                            }
                            overhead_array.append((0, 0, overhead_dict))
                        if component.product_id.product_type == 'miscellaneous':
                            miscellaneous_dict = {
                                'product_id': component.product_id.id,
                                'name': component.product_id.name,
                                'product_type': 'miscellaneous',
                                'product_uom': component.product_uom_id.id,
                                'product_uom_qty': component.product_qty,
                                'price_unit': component.product_id.lst_price,
                            }
                            miscellaneous_array.append((0, 0, miscellaneous_dict))
                        if component.product_id.product_type == 'equipment_and_tools':
                            equipment_and_tools_dict = {
                                'product_id': component.product_id.id,
                                'name': component.product_id.name,
                                'product_type': 'equipment_and_tools',
                                'product_uom': component.product_uom_id.id,
                                'product_uom_qty': component.product_qty,
                                'price_unit': component.product_id.lst_price,
                            }
                            equipment_and_tools_array.append((0, 0, equipment_and_tools_dict))
                    prd_components.prd_labour_lines_ids = labour_array
                    prd_components.prd_material_lines_ids = material_array
                    prd_components.prd_overhead_lines_ids = overhead_array
                    prd_components.prd_miscellaneous_lines_ids = miscellaneous_array
                    prd_components.prd_equipment_lines_ids = equipment_and_tools_array
                self.subproduct_line_id = prd_components.id
                self.price_unit = prd_components.amount_total
                return {
                    'name': _('Components'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'product.components',
                    'res_id': prd_components.id,
                    'view_mode': 'form',
                    'target': 'current',
                }
            else:
                if not self.subproduct_line_id:
                    self.subproduct_line_id = components.id
                return {
                    'name': _('Components'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'product.components',
                    'res_id': components.id,
                    'view_mode': 'form',
                    'target': 'current',
                }

    @api.depends('product_uom_qty', 'margin_rate', 'tax_ids')
    def _compute_amount(self):
        for line in self:
            subtotal = line.product_uom_qty * line.margin_rate
            # if line.discount:
            # subtotal *= (1 - (line.discount / 100.0))
            line.price_subtotal = subtotal
            total_tax = 0.0
            if line.tax_ids:
                taxes = line.tax_ids.compute_all(subtotal, line.currency_id, 1.0, product=line.product_id,
                                                 partner=line.sheet_id.partner_id)
                total_tax = sum(t.get('amount', 0.0) for t in taxes['taxes'])
            line.price_tax = total_tax
            line.price_total = line.price_subtotal + line.price_tax
