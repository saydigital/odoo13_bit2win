# -*- coding: utf-8 -*-

from odoo import models, fields, api
    
class AnalyticAccount(models.Model):
    _inherit ="account.analytic.account"
    
    helpdesk_team_id = fields.Many2one('helpdesk.team','Helpdesk Team',tracking=True)
    date_start= fields.Date('Date Start',tracking=True)
    date_end = fields.Date('Date End',tracking=True)
    final_customer_id = fields.Many2one('res.partner',string="Final Customer")
    
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    date_start= fields.Date('Date Start')
    date_end = fields.Date('Date End')
    helpdesk_team_id = fields.Many2one('helpdesk.team','Helpdesk Team')
    
    
    def _action_confirm(self):
        for order in self:
            if order.helpdesk_team_id and not order.analytic_account_id:
                order._create_analytic_account()
            if order.analytic_account_id and order.helpdesk_team_id:
                if not order.analytic_account_id.date_start :
                    order.analytic_account_id.write(
                                                    {
                                                     'date_start': order.date_start
                                                     }
                                                    )
                order.analytic_account_id.write(
                                                    {
                                                    
                                                     'date_end': order.date_end,
                                                     'helpdesk_team_id': order.helpdesk_team_id
                                                     }
                                                    
                                                    )
                
        return super(SaleOrder,self)._action_confirm()
                
    
                
class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"            
       
    contract_id = fields.Many2one('account.analytic.account',string='Helpdesk Contract')
    
    final_customer_id = fields.Many2one('res.partner',string="Final Customer",related="contract_id.final_customer_id",store=True)
    
class ResPartner(models.Model):
    _inherit = "res.partner"
    
    is_system_integrator = fields.Boolean('Is System Integrator')
    helpdesk_analytic_account_ids= fields.Many2many('account.analytic.account',string='Helpdesk Contract',domain="[('helpdesk_team_id','!=',False)]")
    
    
    def _get_contract_list_tuple(self):
        contracts = []
        if self.is_system_integrator:
            for a in self.helpdesk_analytic_account_ids:
                contracts.append([a.id,a.display_name])
        return contracts
    
    def _get_contract(self,partner_id=False):
        self.ensure_one()
        partner_id = partner_id or self
        if self.parent_id:
            partner_id = self.parent_id
            if self.parent_id.commercial_partner_id:
                partner_id = self.parent_id.commercial_partner_id
                
        return self.env['account.analytic.account'].search([('helpdesk_team_id','!=',False),('date_end','>',fields.Date.today()),('partner_id','=',partner_id.id)],limit=1)