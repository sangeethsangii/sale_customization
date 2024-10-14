from odoo import models, fields

class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    def create_costing_sheet(self):
        ctx = dict(self.env.context)
        ctx.update(
            {
                'default_partner_id': self.partner_id.id,
                'default_opportunity_id': self.id,
            }
        )
        return {
            "name": "Costing Sheet",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "cost.sheet",
            "context": ctx,
            "target": "current",
        }