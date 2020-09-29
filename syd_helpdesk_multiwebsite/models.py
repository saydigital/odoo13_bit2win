from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from random import randint
import datetime
import time
import collections
from odoo.tools.safe_eval import safe_eval

class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'
    
    website_id = fields.Many2one('website',string="Website")
    

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'    
    
    website_id = fields.Many2one('website',string="Website",related="team_id.website_id",store=True)
    
    def _compute_access_url(self):
        super(HelpdeskTicket, self)._compute_access_url()
        for ticket in self:
            if ticket.team_id and ticket.team_id.website_id and ticket.team_id.website_id.domain:
                ticket.access_url = 'https://%s/my/ticket/%s' % (ticket.team_id.website_id.domain,ticket.id)   
                
    def _replace_local_links(self, html, base_url=None):
        base_new_url = base_url
        if self.team_id and self.team_id.website_id and self.team_id.website_id.domain:
            base_new_url = self.team_id.website_id.domain
        return super(HelpdeskTicket,self)._replace_local_links(html,base_new_url)