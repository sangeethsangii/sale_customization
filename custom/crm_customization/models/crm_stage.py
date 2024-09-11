from odoo import models, fields

class CRMStage(models.Model):
    _inherit = 'crm.stage'

    is_restricted = fields.Boolean(string="Is Restricted", default=False)