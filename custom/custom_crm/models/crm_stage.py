from email.policy import default

from odoo import models, api, exceptions, fields
from odoo.exceptions import UserError

class CRMStage(models.Model):
    _inherit = 'crm.stage'

    is_restricted = fields.Boolean(default='False', string="Restricted")

