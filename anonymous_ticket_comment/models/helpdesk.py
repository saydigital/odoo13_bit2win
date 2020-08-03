# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"
    
    communication_user_id = fields.Many2one('res.partner', 'Author')    