from odoo import models, api
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id.is_restricted:
            user = self.env.user
            if not user.has_group('custom_crm_stage_restriction.group_restricted_stage'):
                raise UserError('You are not allowed to move the lead to a restricted stage.')