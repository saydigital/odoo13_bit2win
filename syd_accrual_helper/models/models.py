# -*- coding: utf-8 -*-

from odoo import models, fields, api



class Company(models.Model):
    _inherit = "res.company"
    
    
    temp_income_account_id = fields.Many2one('account.account','Temp Income Account')
    temp_expense_account_id = fields.Many2one('account.account','Temp Expense Account')
    journal_accrual_id = fields.Many2one('account.journal','Journal for Accruals')
    
    
class AccrualHelper(models.AbstractModel):
    _name = "syd_accrual_helper.accrual_mixin"
    _description = "Accrual Mixin"
    
    account_move_ids = fields.Many2many('account.move',string="Accrual")
    accrual_count = fields.Integer('Number of accruals',compute="_accrual_count")
    
    
    
    
    def _accrual_count(self):
        for a in self:
            a.accrual_count = len(a.account_move_ids)
    
    
    def action_accruals(self):
        
        self.ensure_one()
        invoices = self.env['account.move'].search([('id', 'in', self.account_move_ids.ids)])
        action = self.env.ref('account.action_move_journal_line').read()[0]
        action["context"] = {"create": False}
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
class AccountMove(models.Model):
    _name = "account.move"  
    _inherit = ["account.move","syd_accrual_helper.accrual_mixin"]
    
    account_move_ids = fields.Many2many('account.move','move_accrual_rel','origin_id','move_id',string="Accrual")

    def generate_monthly_accrual(self):
        wizard = self.env['syd_accrual_helper.accrual_wizard'].create({
                                                                       'origin_id':self.id,
                                                                       'origin_model':'account.move',
                                                                       'type':'monthly',
                                                                       'debit_credit':'credit' if self.type  in ('out_invoice', 'in_refund') else 'debit',
                                                                       'bring_origin_to_0':True,
                                                                       'post':True,
                                                                       'amount':self.amount_total_signed if self.type not in ('out_invoice', 'in_refund','in_invoice', 'out_refund') else self.amount_untaxed,
                                                                       'date':self.date,
                                                                       'analytic_account_id':self.invoice_line_ids.analytic_account_id.id,
                                                                       'account_id':self.invoice_line_ids.account_id.id if self.type in ('out_invoice', 'in_refund','in_invoice', 'out_refund') else self.line_ids.account_id.id,
                                                                       })
        action = self.env['ir.actions.act_window'].for_xml_id('syd_accrual_helper', 'action_accrual_helper')
        action['domain'] = [('id','=',wizard.id)]
        action['res_id'] = wizard.id
        
        return action
    
    
class AccountMoveLine(models.Model):
    _name = "account.move.line"  
    
    def generate_monthly_accrual(self):
        wizard = self.env['syd_accrual_helper.accrual_wizard'].create({
                                                                       'origin_id':self.move_id.id,
                                                                       'origin_model':'account.move',
                                                                       'type':'monthly',
                                                                       'debit_credit':'credit' if self.move_id.type  in ('out_invoice', 'in_refund') else 'debit',
                                                                       'bring_origin_to_0':True,
                                                                       'post':True,
                                                                       'amount':self.amount_total_signed if self.move_id.type not in ('out_invoice', 'in_refund','in_invoice', 'out_refund') else self.price_subtotal,
                                                                       'date':self.move_id.date,
                                                                       'analytic_account_id':self.analytic_account_id.id,
                                                                       'account_id':self.account_id.id if self.move_id.type in ('out_invoice', 'in_refund','in_invoice', 'out_refund') else self.account_id.id,
                                                                       })
        action = self.env['ir.actions.act_window'].for_xml_id('syd_accrual_helper', 'action_accrual_helper')
        action['domain'] = [('id','=',wizard.id)]
        action['res_id'] = wizard.id
        
        return action