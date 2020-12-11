# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

class CrmTeam(models.Model):
    _inherit = 'crm.team'
    
    
    instance_id = fields.Many2one('consolidated.instance',string="Instance")
    
class CrmStage(models.Model):
    _inherit = 'crm.stage'
    
    
    consolidated_stage_name = fields.Char(string="Stage consolidated name")
        
class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead','consolidated.align_mixin']
    
    instance_id = fields.Many2one('consolidated.instance',string="Instance",related="team_id.instance_id")
    user_name = fields.Char('User name',related="user_id.name",store=True)
    final_customer_id = fields.Many2one('res.partner','Final Customer')
    origin_partner_id = fields.Many2one('res.partner','Origin Contact')
    competition = fields.Selection([('competition','Competition'),('tender','Tender'),('single_source','Single Source')],string="Competition")
    date = fields.Date('Competence date',default=fields.Date.today())
    
    def align_lead_instance(self):
        for a in self:
            a.instance_id.align_lead_instance(a)
        
  



