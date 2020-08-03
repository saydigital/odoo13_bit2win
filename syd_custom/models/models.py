# -*- coding: utf-8 -*-

from odoo import models, fields, api

TICKET_FIELDS = ['name','environment_id','description','contract_id','partner_id','partner_created_id','user_who_found','impact','security_level','priority']

                
class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"            
       
    security_level = fields.Selection([('1','Critical'),('2','Major'),('3','Minor'),('4','Cosmetic')],string="Security Level")
    impact = fields.Selection([('1','Shutting'),('2','Minor')],string="Impact")
    user_who_found = fields.Text(string="User who found the problem")
    partner_created_id= fields.Many2one('res.partner',string="Partner")
    
    
    @api.model
    def website_writable(self):
        model = self.env['ir.model'].sudo().search([('model', '=', 'helpdesk.ticket')])
        model.website_form_access = True
        self.env['ir.model.fields'].sudo().formbuilder_whitelist('helpdesk.ticket',TICKET_FIELDS)
