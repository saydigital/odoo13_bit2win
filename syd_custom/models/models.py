# -*- coding: utf-8 -*-

from odoo import models, fields, api

TICKET_FIELDS = ['name','environment_id','description','contract_id','partner_id','partner_created_id','user_who_found','impact','ticket_type_id','priority']

                
class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"            
       
    user_who_found = fields.Text(string="User who found the problem")
    partner_created_id= fields.Many2one('res.partner',string="Partner")
    impact = fields.Selection([('0','Shutting'),('1','Normal')])
    
    @api.model
    def website_writable(self):
        model = self.env['ir.model'].sudo().search([('model', '=', 'helpdesk.ticket')])
        model.website_form_access = True
        self.env['ir.model.fields'].sudo().formbuilder_whitelist('helpdesk.ticket',TICKET_FIELDS)
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        
        if self.env.context.get('from_home'):
            search_domain = [(True, '=', True)]
            return stages.search(search_domain, order=order)

        return super(HelpdeskTicket,self)._read_group_stage_ids(stages, domain, order)