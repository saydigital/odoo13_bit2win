# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class AccrualHelperWizard(models.TransientModel):
    _name = "syd_accrual_helper.accrual_wizard"
    _description = "Accrual Wizard"

    
    date = fields.Date('Date')
    origin_id = fields.Many2one('syd_accrual_helper.accrual_mixin',string="Origin")
    date_from = fields.Date('Date Start')
    date_to = fields.Date('Date End')
    type=fields.Selection([('month','Month'),('year','Year')],string="Type")
    amount = fields.Float('Amount')
    debit_credit = fields.Selection([('debit','Debit'),('credit','Credit')],string="Credit")
    account_id = fields.Many2one('account.account')
    journal_id= fields.Many2one('account.journal',string="Journal")
    bring_origin_to_0 = fields.Boolean('Brint to 0')
    
    def generate(self):
        AccountMove = self.env['account.move']
        date_from_dt = fields.Date.from_string(self.date_from)
        date_to_dt = fields.Date.from_string(self.date_to)
        
        dates = []
        while (date_from_dt < date_to_dt):
            if (self.type == 'month'):
                
                month = date_from_dt.replace(day=28) + relativedelta(days=4) 
                n_date_to_dt =  month - relativedelta(days=month.day) # Last Day of month
                n_date_from_dt = n_date_to_dt + relativedelta(days=1)
            if (self.type == 'year'):
                n_date_from_dt = date_from_dt + relativedelta(years=1)
                n_date_to_dt = date_from_dt + relativedelta(years=1) - relativedelta(days=1)
            dates += [fields.Date.to_string(date_from_dt)]
            
            date_from_dt = n_date_from_dt
        if not self.amount:
            raise ValidationError(_('Amount Not Valid'))
        if not dates:
            raise ValidationError(_('Period Not Valid'))
        amount_accrued = self.amount/len(dates)
        
        # bring origin to 0
        if self.bring_origin_to_0:
            if self.debit_credit == 'debit':
                move_id = AccountMove.create({
                                    'date':self.origin_id.date if self.origin_id else self.date,
                                    'line_ids':[(0,0,{
                                                      'debit':self.amount,
                                                      'account_id':self.env.user.company_id.temp_expense_account_id.id,
                                                      'name':'Reverse of %s'%self.origin_id.display_name
                                                      }),
                                                (0,0,{
                                                      'credit':self.amount,
                                                      'account_id':self.account_id.id,
                                                      'name':'Reverse of %s'%self.origin_id.display_name
                                                      })
                                                
                                                
                                                ]
                                              })
                
            else:
                move_id = AccountMove.create({
                                    'date':self.origin_id.date,
                                    'line_ids':[(0,0,{
                                                      'debit':self.amount,
                                                      'account_id':self.env.user.company_id.temp_income_account_id.id,
                                                      'name':'Reverse of %s'%self.origin_id.display_name
                                                      }),
                                                (0,0,{
                                                      'credit':self.amount,
                                                      'account_id':self.account_id.id,
                                                      'name':'Reverse of %s'%self.origin_id.display_name
                                                      })
                                                
                                                
                                                ]
                                    
                                    })
            if self.origin_id:
                self.origin_id.account_move_ids = [(4,move_id.id)]
        for d in dates:
            if self.debit_credit == 'debit':
                move_id = AccountMove.create({
                                'date':d,
                                'line_ids':[(0,0,{
                                                  'debit':amount_accrued,
                                                  'account_id':self.env.user.company_id.temp_income_account_id.id,
                                                  'name':'Reverse of %s'%self.origin_id.display_name
                                                  }),
                                            (0,0,{
                                                  'credit':amount_accrued,
                                                  'account_id':self.account_id.id,
                                                  'name':'Reverse of %s'%self.origin_id.display_name
                                                  })
                                            
                                            
                                            ]
                                
                                })
            else:
                move_id = AccountMove.create({
                                'date':d,
                                'line_ids':[(0,0,{
                                                  'credit':amount_accrued,
                                                  'account_id':self.env.user.company_id.temp_income_account_id.id,
                                                  'name':'Reverse of %s'%self.origin_id.display_name
                                                  }),
                                            (0,0,{
                                                  'debit':amount_accrued,
                                                  'account_id':self.account_id.id,
                                                  'name':'Reverse of %s'%self.origin_id.display_name
                                                  })
                                            
                                            
                                            ]
                                
                                })
            if self.origin_id:
                self.origin_id.account_move_ids = [(4,move_id.id)] 
            
        
        
        