from odoo import models, api, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # @api.multi
    # def write(self, vals):
    #     stage_id = vals.get('stage_id')
    #     if stage_id:
    #         stage = self.env['crm.stage'].browse(stage_id)
    #         if stage.is_restricted:
    #             # You can add the validation to allow restricted stage movement only for a specific group.
    #             if not self.env.user.has_group('your_module_name.group_restricted_stage'):
    #                 raise UserError(_("You are not allowed to move leads to a restricted stage."))
    #     return super(CrmLead, self).write(vals)