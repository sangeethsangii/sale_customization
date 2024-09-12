from odoo import models, api , exceptions
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    @api.constrains('stage_id')
    def _check_stage_access(self):
        for lead in self:
            if lead.stage_id.is_restricted :
                if not self.env.user.has_group('custom_crm.group_manage_restricted_stage'):
                    raise exceptions.UserError("You do not have permission to access this restricted stage.")
