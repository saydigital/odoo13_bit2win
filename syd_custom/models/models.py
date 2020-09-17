# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError

TICKET_FIELDS = ['partner_created_id','environment_id_desc','name','release_id','reported_by','access_granted','level','environment_id','description','contract_id','partner_id','partner_created_id','user_who_found','impact','ticket_type_id','priority','granted_user']


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    reported_by = fields.Many2one('helpdesk.reported','Helpdesk Role')
    
    
    
    
class HelpdeskReported(models.Model):
    _name = "helpdesk.reported"
    _description = "Reported"
    
    name = fields.Char('Reported')
    sequence = fields.Integer('Sequence')
                
    
class HelpdeskRelease(models.Model):
    _name = "helpdesk.release"
    _description = "Release"
    
    name = fields.Char('Release')
    sequence = fields.Integer('Sequence')
                    

class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    name_for_customer = fields.Char('Name for customer')
    flag_before_email = fields.Boolean('Flag before email')   
    flag_after_email = fields.Boolean('Flag before email')
            
class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"            
       
    user_who_found = fields.Text(string="User who found the problem",tracking=True)
    partner_created_id= fields.Many2one('res.partner',string="Reported by",tracking=True,default=lambda self: self.env.user.partner_id.id)
    impact = fields.Selection([('0','Blocking'),('1','Non Blocking')],default="0",tracking=True)
    access_granted = fields.Boolean('Access Granted',tracking=True)
    granted_user = fields.Text(string="Granted User",tracking=True)
    level = fields.Selection([('1','Level 1'),('2','Level 2')],default="1",tracking=True)
    fixing = fields.Boolean('Fixing',tracking=True)
    pay_attention = fields.Boolean('Pay Attention',tracking=True)
    reason_why_id = fields.Char('Reason',tracking=True)
    release_id = fields.Many2one('helpdesk.release','Release',tracking=True)
    reported_by = fields.Many2one('helpdesk.reported','Reported by',related="partner_id.reported_by",tracking=True)
    environment_id_desc = fields.Text(string="Environment Description",tracking=True)
    date_fix = fields.Date('Planned Fix Date',tracking=True)

    def set_level_1(self):
        self.write({'level':'1'})
        
    def set_level_2(self):
        self.write({'level':'2'})
        
    def set_fixing(self):
        self.write({'fixing':True})
        
    def set_no_fixing(self):
        self.write({'fixing':False})
        
    def set_pay_attention(self):
        self.write({'pay_attention':True})
        
    def no_pay_attention(self):
        self.write({'pay_attention':False})
        
    @api.model
    def website_writable(self):
        model = self.env['ir.model'].sudo().search([('model', '=', 'helpdesk.ticket')])
        model.website_form_access = True
        self.env['ir.model.fields'].sudo().formbuilder_whitelist('helpdesk.ticket',TICKET_FIELDS)
    
    
    def create(self,vals):
        tickets = super(HelpdeskTicket, self).create(vals)
        for ticket in tickets:
            if ticket.partner_created_id.id != ticket.partner_id.id:
                ticket.message_subscribe(partner_ids=ticket.partner_created_id.ids)
        return tickets
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        
        if self.env.context.get('from_home'):
            search_domain = [(True, '=', True)]
            return stages.search(search_domain, order=order)

        return super(HelpdeskTicket,self)._read_group_stage_ids(stages, domain, order)