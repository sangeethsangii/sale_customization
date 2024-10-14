from odoo import fields, models, api, _


class ProductComponents(models.Model):
    _name = "product.components"
    _description = "Product Components"
    _rec_name = "product_id"

    product_id = fields.Many2one('product.product', string="Product", required=True, domain=[
        ('product_type', 'not in', ('material', 'labour', 'overhead', 'miscellaneous'))])
    cost_sheet_line_id = fields.Many2one('cost.sheet.line', copy=False)
    bom_id = fields.Many2one('mrp.bom', copy=False)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)
    total_material_estimation = fields.Monetary(string="Total Material Estimation", store=True,
                                                compute='_compute_material_amounts')
    total_labour_estimation = fields.Monetary(string="Total Labour Estimation", store=True,
                                              compute='_compute_labour_amounts')
    total_overhead_estimation = fields.Monetary(string="Total Overhead Estimation", store=True,
                                                compute='_compute_overhead_amounts')
    total_miscellaneous_estimation = fields.Monetary(string="Total Miscellaneous Estimation", store=True,
                                                     compute='_compute_miscellaneous_amounts')
    total_equipment_and_tools_estimation = fields.Monetary(string="Total Equipment & Tools Estimation", store=True,
                                                           compute='_compute_equipment_and_tools_estimation')
    amount_total = fields.Monetary(string="Total", store=True, compute='_compute_total_amount')
    prd_material_lines_ids = fields.One2many('product.components.material', 'comp_id', string="Material Lines")
    prd_labour_lines_ids = fields.One2many('product.components.labour', 'comp_id', string="Labour Lines")
    prd_overhead_lines_ids = fields.One2many('product.components.overhead', 'comp_id', string="Overhead Lines")
    prd_miscellaneous_lines_ids = fields.One2many('product.components.miscellaneous', 'comp_id',
                                                  string="Miscellaneous Lines")
    prd_equipment_lines_ids = fields.One2many('product.components.equipment.tools', 'comp_id',
                                              string="Equipment & Tools")

    @api.onchange('amount_total')
    def _onchange_amount_total(self):
        self.cost_sheet_line_id.price_unit = self.amount_total

    @api.depends('prd_material_lines_ids.price_subtotal')
    def _compute_material_amounts(self):
        for order in self:
            order_lines = order.prd_material_lines_ids
            if order_lines:
                total_material_estimation = sum(order_lines.mapped('price_subtotal'))
                order.total_material_estimation = total_material_estimation

    @api.depends('prd_labour_lines_ids.price_subtotal')
    def _compute_labour_amounts(self):
        for order in self:
            order_lines = order.prd_labour_lines_ids
            if order_lines:
                total_labour_estimation = sum(order_lines.mapped('price_subtotal'))
                order.total_labour_estimation = total_labour_estimation

    @api.depends('prd_overhead_lines_ids.price_subtotal')
    def _compute_overhead_amounts(self):
        for order in self:
            order_lines = order.prd_overhead_lines_ids
            if order_lines:
                total_overhead_estimation = sum(order_lines.mapped('price_subtotal'))
                order.total_overhead_estimation = total_overhead_estimation

    @api.depends('prd_miscellaneous_lines_ids.price_subtotal')
    def _compute_miscellaneous_amounts(self):
        for order in self:
            order_lines = order.prd_miscellaneous_lines_ids
            if order_lines:
                total_miscellaneous_estimation = sum(order_lines.mapped('price_subtotal'))
                order.total_miscellaneous_estimation = total_miscellaneous_estimation

    @api.depends('prd_equipment_lines_ids.price_subtotal')
    def _compute_equipment_and_tools_estimation(self):
        for order in self:
            order_lines = order.prd_equipment_lines_ids
            if order_lines:
                total_equipment_and_tools_estimation = sum(order_lines.mapped('price_subtotal'))
                order.total_equipment_and_tools_estimation = total_equipment_and_tools_estimation

    @api.depends('total_material_estimation', 'total_labour_estimation', 'total_overhead_estimation',
                 'total_miscellaneous_estimation', 'total_equipment_and_tools_estimation')
    def _compute_total_amount(self):
        for order in self:
            total_material_estimation = order.total_material_estimation or 0.0
            total_labour_estimation = order.total_labour_estimation or 0.0
            total_overhead_estimation = order.total_overhead_estimation or 0.0
            total_miscellaneous_estimation = order.total_miscellaneous_estimation or 0.0
            total_equipment_and_tools_estimation = order.total_equipment_and_tools_estimation or 0.0
            order.amount_total = total_material_estimation + total_labour_estimation + total_overhead_estimation + total_miscellaneous_estimation + total_equipment_and_tools_estimation


class ProductComponentsMaterial(models.Model):
    _name = "product.components.material"
    _description = "Product Components Material"

    product_id = fields.Many2one('product.product', string="Product", required=True,
                                 domain=[('product_type', '=', 'material')])
    comp_id = fields.Many2one('product.components', string="Components", copy=False)
    name = fields.Char("Description", required=True)
    product_type = fields.Selection([
        ('material', 'Material'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('miscellaneous', 'Miscellaneous'),
    ], string="Type", related='product_id.product_type', store=1)
    product_uom_qty = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure', default=1.0,
        required=True)
    product_uom = fields.Many2one(
        comodel_name='uom.uom', domain="[('category_id', '=', product_uom_category_id)]",
        string="Unit of Measure", ondelete='restrict')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    price_unit = fields.Float(
        string="Unit Price",
        digits='Product Price',
        required=True)
    discount = fields.Float(
        string="Discount (%)",
        digits='Discount',
        store=True, readonly=False)
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.product_uom = self.product_id.uom_id.id
        self.price_unit = self.product_id.lst_price

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for res in records:
            if res.comp_id:
                bom_id = res.comp_id.bom_id
                if not bom_id:
                    bom_id = self.env['mrp.bom'].search(
                        [('product_tmpl_id', '=', res.comp_id.product_id.product_tmpl_id.id)],
                        limit=1)
                    if not bom_id:
                        bom_id = self.env['mrp.bom'].create({
                            'product_tmpl_id': res.comp_id.product_id.product_tmpl_id.id,
                        })
                    res.comp_id.bom_id = bom_id.id
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == res.product_id.id)
                if not bom_line_id:
                    bom_line_vals = {
                        'product_id': res.product_id.id,
                        'product_uom_id': res.product_uom.id,
                        'product_qty': res.product_uom_qty,
                        'bom_id': bom_id.id,
                    }
                    bom_line_id = self.env['mrp.bom.line'].create(bom_line_vals)
        return records

    def unlink(self):
        for record in self:
            bom_id = record.comp_id.bom_id
            if bom_id:
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == record.product_id.id)
                for bom_line in bom_line_id:
                    bom_line.unlink()
        return super().unlink()

    @api.depends('product_uom_qty', 'discount', 'price_unit')
    def _compute_amount(self):
        for line in self:
            discount = line.discount or 0.0
            product_uom_qty = line.product_uom_qty or 0.0
            price_unit = line.price_unit or 0.0
            subtotal = price_unit * product_uom_qty * (1 - (discount / 100))
            line.price_subtotal = subtotal


class ProductComponentsLabour(models.Model):
    _name = "product.components.labour"
    _description = "Product Components Labour"

    product_id = fields.Many2one('product.product', string="Product", required=True,
                                 domain=[('product_type', '=', 'labour')])
    comp_id = fields.Many2one('product.components', string="Components", copy=False)
    name = fields.Char("Description", required=True)
    product_type = fields.Selection([
        ('material', 'Material'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('miscellaneous', 'Miscellaneous'),
    ], string="Type", related='product_id.product_type', store=1)
    product_uom_qty = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure', default=1.0,
        required=True)
    product_uom = fields.Many2one(
        comodel_name='uom.uom', domain="[('category_id', '=', product_uom_category_id)]",
        string="Unit of Measure", ondelete='restrict')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    price_unit = fields.Float(
        string="Unit Price",
        digits='Product Price',
        required=True)
    discount = fields.Float(
        string="Discount (%)",
        digits='Discount',
        store=True, readonly=False)
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.product_uom = self.product_id.uom_id.id
        self.price_unit = self.product_id.lst_price

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for res in records:
            if res.comp_id:
                bom_id = res.comp_id.bom_id
                if not bom_id:
                    bom_id = self.env['mrp.bom'].search(
                        [('product_tmpl_id', '=', res.comp_id.product_id.product_tmpl_id.id)],
                        limit=1)
                    if not bom_id:
                        bom_id = self.env['mrp.bom'].create({
                            'product_tmpl_id': res.comp_id.product_id.product_tmpl_id.id,
                        })
                    res.comp_id.bom_id = bom_id.id
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == res.product_id.id)
                if not bom_line_id:
                    bom_line_vals = {
                        'product_id': res.product_id.id,
                        'product_uom_id': res.product_uom.id,
                        'product_qty': res.product_uom_qty,
                        'bom_id': bom_id.id,
                    }
                    bom_line_id = self.env['mrp.bom.line'].create(bom_line_vals)
        return records

    def unlink(self):
        for record in self:
            bom_id = record.comp_id.bom_id
            if bom_id:
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == record.product_id.id)
                for bom_line in bom_line_id:
                    bom_line.unlink()
        return super().unlink()

    @api.depends('product_uom_qty', 'discount', 'price_unit')
    def _compute_amount(self):
        for line in self:
            discount = line.discount or 0.0
            product_uom_qty = line.product_uom_qty or 0.0
            price_unit = line.price_unit or 0.0
            subtotal = price_unit * product_uom_qty * (1 - (discount / 100))
            line.price_subtotal = subtotal


class ProductComponentsOverhead(models.Model):
    _name = "product.components.overhead"
    _description = "Product Components Overhead"

    product_id = fields.Many2one('product.product', string="Product", required=True,
                                 domain=[('product_type', '=', 'overhead')])
    comp_id = fields.Many2one('product.components', string="Components", copy=False)
    name = fields.Char("Description", required=True)
    product_type = fields.Selection([
        ('material', 'Material'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('miscellaneous', 'Miscellaneous'),
    ], string="Type", related='product_id.product_type', store=1)
    product_uom_qty = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure', default=1.0,
        required=True)
    product_uom = fields.Many2one(
        comodel_name='uom.uom', domain="[('category_id', '=', product_uom_category_id)]",
        string="Unit of Measure", ondelete='restrict')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    price_unit = fields.Float(
        string="Unit Price",
        digits='Product Price',
        required=True)
    discount = fields.Float(
        string="Discount (%)",
        digits='Discount',
        store=True, readonly=False)
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.product_uom = self.product_id.uom_id.id
        self.price_unit = self.product_id.lst_price

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for res in records:
            if res.comp_id:
                bom_id = res.comp_id.bom_id
                if not bom_id:
                    bom_id = self.env['mrp.bom'].search(
                        [('product_tmpl_id', '=', res.comp_id.product_id.product_tmpl_id.id)],
                        limit=1)
                    if not bom_id:
                        bom_id = self.env['mrp.bom'].create({
                            'product_tmpl_id': res.comp_id.product_id.product_tmpl_id.id,
                        })
                    res.comp_id.bom_id = bom_id.id
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == res.product_id.id)
                if not bom_line_id:
                    bom_line_vals = {
                        'product_id': res.product_id.id,
                        'product_uom_id': res.product_uom.id,
                        'product_qty': res.product_uom_qty,
                        'bom_id': bom_id.id,
                    }
                    bom_line_id = self.env['mrp.bom.line'].create(bom_line_vals)
        return records

    def unlink(self):
        for record in self:
            bom_id = record.comp_id.bom_id
            if bom_id:
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == record.product_id.id)
                for bom_line in bom_line_id:
                    bom_line.unlink()
        return super().unlink()

    @api.depends('product_uom_qty', 'discount', 'price_unit')
    def _compute_amount(self):
        for line in self:
            discount = line.discount or 0.0
            product_uom_qty = line.product_uom_qty or 0.0
            price_unit = line.price_unit or 0.0
            subtotal = price_unit * product_uom_qty * (1 - (discount / 100))
            line.price_subtotal = subtotal


class ProductComponentsMiscellaneous(models.Model):
    _name = "product.components.miscellaneous"
    _description = "Product Components Miscellaneous"

    product_id = fields.Many2one('product.product', string="Product", required=True,
                                 domain=[('product_type', '=', 'miscellaneous')])
    comp_id = fields.Many2one('product.components', string="Components", copy=False)
    name = fields.Char("Description", required=True)
    product_type = fields.Selection([
        ('material', 'Material'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('miscellaneous', 'Miscellaneous'),
    ], string="Type", related='product_id.product_type', store=1)
    product_uom_qty = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure', default=1.0,
        required=True)
    product_uom = fields.Many2one(
        comodel_name='uom.uom', domain="[('category_id', '=', product_uom_category_id)]",
        string="Unit of Measure", ondelete='restrict')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    price_unit = fields.Float(
        string="Unit Price",
        digits='Product Price',
        required=True)
    discount = fields.Float(
        string="Discount (%)",
        digits='Discount',
        store=True, readonly=False)
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.product_uom = self.product_id.uom_id.id
        self.price_unit = self.product_id.lst_price

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for res in records:
            if res.comp_id:
                bom_id = res.comp_id.bom_id
                if not bom_id:
                    bom_id = self.env['mrp.bom'].search(
                        [('product_tmpl_id', '=', res.comp_id.product_id.product_tmpl_id.id)],
                        limit=1)
                    if not bom_id:
                        bom_id = self.env['mrp.bom'].create({
                            'product_tmpl_id': res.comp_id.product_id.product_tmpl_id.id,
                        })
                    res.comp_id.bom_id = bom_id.id
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == res.product_id.id)
                if not bom_line_id:
                    bom_line_vals = {
                        'product_id': res.product_id.id,
                        'product_uom_id': res.product_uom.id,
                        'product_qty': res.product_uom_qty,
                        'bom_id': bom_id.id,
                    }
                    bom_line_id = self.env['mrp.bom.line'].create(bom_line_vals)
        return records

    def unlink(self):
        for record in self:
            bom_id = record.comp_id.bom_id
            if bom_id:
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == record.product_id.id)
                for bom_line in bom_line_id:
                    bom_line.unlink()
        return super().unlink()

    @api.depends('product_uom_qty', 'discount', 'price_unit')
    def _compute_amount(self):
        for line in self:
            discount = line.discount or 0.0
            product_uom_qty = line.product_uom_qty or 0.0
            price_unit = line.price_unit or 0.0
            subtotal = price_unit * product_uom_qty * (1 - (discount / 100))
            line.price_subtotal = subtotal


class ProductComponentsEquipmentTools(models.Model):
    _name = "product.components.equipment.tools"
    _description = "Product Components Equipment and Tools"

    product_id = fields.Many2one('product.product', string="Product", required=True,
                                 domain=[('product_type', '=', 'equipment_and_tools')])
    comp_id = fields.Many2one('product.components', string="Components", copy=False)
    name = fields.Char("Description", required=True)
    product_type = fields.Selection([
        ('material', 'Material'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('miscellaneous', 'Miscellaneous'),
        ('equipment_and_tools', 'Equipment & Tools'),
    ], string="Type", related='product_id.product_type', store=1)
    product_uom_qty = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure', default=1.0,
        required=True)
    product_uom = fields.Many2one(
        comodel_name='uom.uom', domain="[('category_id', '=', product_uom_category_id)]",
        string="Unit of Measure", ondelete='restrict')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    price_unit = fields.Float(
        string="Unit Price",
        digits='Product Price',
        required=True)
    discount = fields.Float(
        string="Discount (%)",
        digits='Discount',
        store=True, readonly=False)
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.product_uom = self.product_id.uom_id.id
        self.price_unit = self.product_id.lst_price

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for res in records:
            if res.comp_id:
                bom_id = res.comp_id.bom_id
                if not bom_id:
                    bom_id = self.env['mrp.bom'].search(
                        [('product_tmpl_id', '=', res.comp_id.product_id.product_tmpl_id.id)],
                        limit=1)
                    if not bom_id:
                        bom_id = self.env['mrp.bom'].create({
                            'product_tmpl_id': res.comp_id.product_id.product_tmpl_id.id,
                        })
                    res.comp_id.bom_id = bom_id.id
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == res.product_id.id)
                if not bom_line_id:
                    bom_line_vals = {
                        'product_id': res.product_id.id,
                        'product_uom_id': res.product_uom.id,
                        'product_qty': res.product_uom_qty,
                        'bom_id': bom_id.id,
                    }
                    bom_line_id = self.env['mrp.bom.line'].create(bom_line_vals)
        return records

    def unlink(self):
        for record in self:
            bom_id = record.comp_id.bom_id
            if bom_id:
                bom_line_id = bom_id.bom_line_ids.filtered(lambda s: s.product_id.id == record.product_id.id)
                for bom_line in bom_line_id:
                    bom_line.unlink()
        return super().unlink()

    @api.depends('product_uom_qty', 'discount', 'price_unit')
    def _compute_amount(self):
        for line in self:
            discount = line.discount or 0.0
            product_uom_qty = line.product_uom_qty or 0.0
            price_unit = line.price_unit or 0.0
            subtotal = price_unit * product_uom_qty * (1 - (discount / 100))
            line.price_subtotal = subtotal


            
