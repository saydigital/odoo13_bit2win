# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Company(models.Model):
    _inherit = "res.company"
    
    
    temp_income_account_id = fields.Many2one('account.account','Temp Income Account')
    temp_expense_account_id = fields.Many2one('account.account','Temp Expense Account')
    
class AccrualHelper(models.AbstractModel):
    _name = "syd_accrual_helper.accrual_mixin"
    _description = "Accrual Mixin"
    
    account_move_ids = fields.Many2many('account.move',string="Accrual")
    date= fields.Date('Date')           

    