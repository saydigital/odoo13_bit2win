# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = ["sale.subscription","syd_accrual_helper.accrual_mixin"]
    
    def generate_monthly_accrual(self):
        wizard = self.env['syd_accrual_helper.accrual_wizard'].create({
                                                                       'origin_id':self.id,
                                                                       'origin_model':'sale.subscription',
                                                                       'date_from':self.date_start,
                                                                       'date_to':self.date,
                                                                       'type':'monthly',
                                                                       'amount':self.recurring_total,
                                                                       'debit_credit':'credit',
                                                                       'bring_origin_to_0':False,
                                                                       'post':True,
                                                                       'divide':'monthly' != self.recurring_rule_type
                                                                       })
        action = self.env['ir.actions.act_window'].for_xml_id('syd_accrual_helper', 'action_accrual_helper')
        action['domain'] = [('id','=',wizard.id)]
        action['res_id'] = wizard.id
        
        return action

class AccountMove(models.Model):
    _inherit = "account.move"    
    
    
    def generate_monthly_accrual(self):
        for a in self:
            if a.invoice_line_ids.subscription_id:
                for i in a.invoice_line_ids:
                    wizard = self.env['syd_accrual_helper.accrual_wizard'].create({
                                                                                   'origin_id':a.id,
                                                                                   'origin_model':'account.move',
                                                                                   'date_from':i.subscription_start_date,
                                                                                   'date_to':i.subscription_end_date,
                                                                                   'account_id':i.account_id.id,
                                                                                   'type':'monthly',
                                                                                   'amount':i.price_subtotal,
                                                                                   'debit_credit':'credit',
                                                                                   'bring_origin_to_0':True,
                                                                                   'post':True,
                                                                                   'divide':'monthly' != i.subscription_id.recurring_rule_type
                                                                                   
                                                                                   })
                    wizard.generate()
            else:
                return super(AccountMove,self).generate_monthly_accrual()
        
        
        return True
    
    