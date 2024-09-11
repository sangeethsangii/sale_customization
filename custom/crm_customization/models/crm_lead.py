from odoo import models, api
from odoo.exceptions import AccessError

class CRMLead(models.Model):
    _inherit = 'crm.lead',
    _inherit = 'crm.stage'

    # @api.multi
    # def write(self, vals):
    #     stage_id = vals.get('stage_id')
    #     if stage_id:
    #         stage = self.env['crm.stage'].browse(stage_id)
    #         if stage.is_restricted and not self.env.user.has_group('your_module.group_crm_restricted'):
    #             raise AccessError("You cannot move this lead to a restricted stage.")
    #     return super(CRMLead, self).write(vals)