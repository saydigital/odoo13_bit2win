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
                                                                       'divide':'monthly' != self.recurring_rule_type,
                                                                       'analytic_account_id':self.analytic_account_id.id
                                                                       })
        action = self.env['ir.actions.act_window'].for_xml_id('syd_accrual_helper', 'action_accrual_helper')
        action['domain'] = [('id','=',wizard.id)]
        action['res_id'] = wizard.id
        
        return action
    
    def _prepare_invoice_lines(self, fiscal_position):
        self.ensure_one()
        if self.date:
            revenue_date_start = self.recurring_next_date
            revenue_date_stop = self.date
            return [(0, 0, self._prepare_invoice_line(line, fiscal_position, revenue_date_start, revenue_date_stop)) for line in self.recurring_invoice_line_ids]
        else:
            return super(SaleSubscription,self)._prepare_invoice_lines(fiscal_position)

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
                                                                                   'analytic_account_id':i.analytic_account_id.id,
                                                                                   'debit_credit':'credit',
                                                                                   'bring_origin_to_0':True,
                                                                                   'post':False,
                                                                                   'divide':'monthly' != i.subscription_id.recurring_rule_type
                                                                                   
                                                                                   })

            else:
                return super(AccountMove,self).generate_monthly_accrual()
        
        
        return True
    
    