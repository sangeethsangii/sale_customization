from email.policy import default

from odoo import models, api, exceptions, fields
from odoo.exceptions import UserError

class CRMStage(models.Model):
    _inherit = 'crm.stage'

    is_restricted = fields.Boolean(default='False', string="Restricted")

    @api.constrains('is_restricted')
    def _check_is_restricted_move(self):
        if self.is_restricted:
            user = self.env.user
            if not user.has_group('custom_crm_stage_restriction.group_restricted_stage'):
                raise UserError('You are not allowed to drag restricted stages.')




