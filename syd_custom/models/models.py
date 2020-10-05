# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

TICKET_FIELDS = ['partner_created_id', 'environment_id_desc', 'name', 'release_id', 'reported_by', 'access_granted', 'level', 'environment_id', 'description', 'contract_id', 'partner_id', 'partner_created_id', 'user_who_found', 'impact', 'ticket_type_id', 'priority', 'granted_user', 'module', 'package','team_id']


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    reported_by = fields.Many2one('helpdesk.reported', 'Helpdesk Role')
    #administrative_user = fields.Boolean('Administrative user')

    
class HelpdeskReported(models.Model):
    _name = "helpdesk.reported"
    _description = "Reported"
    _order = 'sequence'
    
    name = fields.Char('Reported')
    sequence = fields.Integer('Sequence')
                
    
class HelpdeskRelease(models.Model):
    _name = "helpdesk.release"
    _description = "Release"
    _order = 'sequence'
    
    name = fields.Char('Release')
    sequence = fields.Integer('Sequence')
                    
class HelpdeskPackage(models.Model):
    _name = "helpdesk.package"
    _description = "package"
    _order = 'sequence'
    
    name = fields.Char('Package')
    sequence = fields.Integer('Sequence')                    

class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    name_for_customer = fields.Char('Name for customer')
    flag_before_email = fields.Boolean('Flag before email')   
    flag_after_email = fields.Boolean('Flag after email')

            
class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"            
       
    user_who_found = fields.Char(string="Business User", tracking=True)
    origin = fields.Text(string="Origin", tracking=True)
    partner_created_id = fields.Many2one('res.partner', string="Reported by", tracking=True, default=lambda self: self.env.user.partner_id.id)
    impact = fields.Selection([('0', 'Blocking'), ('1', 'Non Blocking')], default="0", tracking=True)
    granted_user = fields.Char(string="Granted User", tracking=True)
    level = fields.Selection([('1', 'Level 1'), ('2', 'Level 2')], default="1", tracking=True)
    fixing = fields.Boolean('Fixing', tracking=True)
    pay_attention = fields.Boolean('Pay Attention', tracking=True)
    reason_why_id = fields.Char('Reason', tracking=True)
    release_id = fields.Many2one('helpdesk.release', 'Release', tracking=True)
    package_id = fields.Many2one('helpdesk.package', 'Package', tracking=True)
    reported_by = fields.Many2one('helpdesk.reported', 'Reported by role', related="partner_id.reported_by", tracking=True)
    environment_id_desc = fields.Char(string="Org ID", tracking=True)
    date_fix = fields.Date('Planned Fix Date', tracking=True)
    module = fields.Selection([('0', 'Core'), ('1', 'Bulk order'), ('2', 'E-signature'), ('3', 'Archetypes'), ('4', 'Store'), ('5', 'Zuora connector'), ('6', 'Sapisu-connector'),
                               ('7', 'Utility'), ('8', 'Cost-simulator'), ('9', 'Cost-simulator'), ('10', 'External-catalog'), ('11', 'Flow'), ('12', 'Loyalty'), ('13', 'Cart-api'), ('14', 'Ssymphony')], default="0", tracking=True)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *,
                     body='', subject=None, message_type='notification',
                     email_from=None, author_id=None, parent_id=False,
                     subtype_id=False, subtype=None, partner_ids=None, channel_ids=None,
                     attachments=None, attachment_ids=None,
                     add_sign=True, record_name=False,
                     **kwargs):
        message = super(HelpdeskTicket, self).message_post(body=body, subject=subject, message_type=message_type,
                     email_from=email_from, author_id=author_id, parent_id=parent_id,
                     subtype_id=subtype_id, subtype=subtype, partner_ids=partner_ids, channel_ids=channel_ids,
                     attachments=attachments, attachment_ids=attachment_ids,
                     add_sign=add_sign, record_name=record_name,
                     **kwargs)
        if  self._is_user_from_frontend() and bool(message_type == 'comment') and bool(subtype == 'mt_comment') and self.stage_id.flag_before_email:
            stage_id = self.env['helpdesk.stage'].search([('flag_after_email', '=', True)], limit=1)
            if stage_id:
                self.stage_id = stage_id.id
        return message
    
    def _is_user_from_frontend(self):
        # if 1 user is from backend
        return (bool(8 in self.env.user.groups_id.ids))
    
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
        self.env['ir.model.fields'].sudo().formbuilder_whitelist('helpdesk.ticket', TICKET_FIELDS)

    @api.model
    def create(self, vals):
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

        return super(HelpdeskTicket, self)._read_group_stage_ids(stages, domain, order)
