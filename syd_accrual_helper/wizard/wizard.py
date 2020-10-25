# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class AccrualHelperWizard(models.TransientModel):
    _name = "syd_accrual_helper.accrual_wizard"
    _description = "Accrual Wizard"

    
    date = fields.Date('Date')
    origin_model = fields.Char('Model')
    origin_id = fields.Many2one('syd_accrual_helper.accrual_mixin',string="Origin")
    date_from = fields.Date('Date Start')
    date_to = fields.Date('Date End')
    type=fields.Selection([('monthly','Month'),('yearly','Year')],string="Type")
    amount = fields.Float('Amount')
    debit_credit = fields.Selection([('debit','Debit'),('credit','Credit')],string="Credit")
    account_id = fields.Many2one('account.account')
    journal_id= fields.Many2one('account.journal',string="Journal",default=lambda self: self.env.user.company_id.journal_accrual_id.id)
    bring_origin_to_0 = fields.Boolean('Bring to 0',default=False)
    post = fields.Boolean('Post',default=True)
    divide = fields.Boolean('Divide',default=True)
    
    def generate(self):
        AccountMove = self.env['account.move']
        date_from_dt = fields.Date.from_string(self.date_from)
        date_to_dt = fields.Date.from_string(self.date_to)
        if self.origin_id:
            origin_id = self.env[self.origin_model].browse(self.origin_id.id)
        else:
            origin_id = False
        dates = []
        while (date_from_dt < date_to_dt):
            if (self.type == 'monthly'):
                
                month = date_from_dt.replace(day=28) + relativedelta(days=4) 
                n_date_to_dt =  month - relativedelta(days=month.day) # Last Day of month
                n_date_from_dt = n_date_to_dt + relativedelta(days=1)
            if (self.type == 'yearly'):
                n_date_from_dt = date_from_dt + relativedelta(years=1)
                n_date_to_dt = date_from_dt + relativedelta(years=1) - relativedelta(days=1)
            dates += [fields.Date.to_string(date_from_dt)]
            
            date_from_dt = n_date_from_dt
        if not self.amount:
            raise ValidationError(_('Amount Not Valid'))
        if not dates:
            raise ValidationError(_('Period Not Valid'))
        
        amount_accrued = self.amount/(len(dates) if len(dates)<=12 else 12) if self.divide else self.amount
        
        # bring origin to 0
        if self.bring_origin_to_0:
            if self.debit_credit == 'debit':
                move_id = AccountMove.create({
                                    'date':origin_id.date if origin_id else self.date,
                                    'ref':origin_id.display_name,
                                    'journal_id':self.journal_id.id,
                                    'type':'entry',
                                    'line_ids':[(0,0,{
                                                      'credit':self.amount,
                                                      'account_id':self.env.user.company_id.temp_expense_account_id.id,
                                                      'name':'Accrual to 0 of %s'%origin_id.display_name
                                                      }),
                                                (0,0,{
                                                      'debit':self.amount,
                                                      'account_id':self.account_id.id,
                                                      'name':'/'
                                                      })
                                                
                                                
                                                ]
                                              })
                if self.post:
                    move_id.action_post()
                
            else:
                move_id = AccountMove.create({
                                    'date':origin_id.date,
                                    'ref':origin_id.display_name,
                                    'journal_id':self.journal_id.id,
                                    'type':'entry',
                                    'line_ids':[(0,0,{
                                                      'credit':self.amount,
                                                      'account_id':self.env.user.company_id.temp_income_account_id.id,
                                                      'name':'/'
                                                      }),
                                                (0,0,{
                                                      'debit':self.amount,
                                                      'account_id':self.account_id.id,
                                                      'name':'Accrual to 0 of %s'%origin_id.display_name
                                                      })
                                                
                                                
                                                ]
                                    
                                    })
                if self.post:
                    move_id.action_post()
            if origin_id:
                origin_id.account_move_ids = [(4,move_id.id)]
        for d in dates:
            if self.debit_credit == 'debit':
                move_id = AccountMove.create({
                                'date':d,
                                'ref':origin_id.display_name,
                                'journal_id':self.journal_id.id,
                                'type':'entry',
                                'line_ids':[(0,0,{
                                                  'credit':amount_accrued,
                                                  'account_id':self.env.user.company_id.temp_income_account_id.id,
                                                  'name':'Accrual of %s'%origin_id.display_name
                                                  }),
                                            (0,0,{
                                                  'debit':amount_accrued,
                                                  'account_id':self.account_id.id,
                                                  'name':'/'
                                                  })
                                            
                                            
                                            ]
                                
                                })
                if self.post:
                    move_id.action_post()
            else:
                move_id = AccountMove.create({
                                'date':d,
                                'ref':origin_id.display_name,
                                'journal_id':self.journal_id.id,
                                'type':'entry',
                                'line_ids':[(0,0,{
                                                  'debit':amount_accrued,
                                                  'account_id':self.env.user.company_id.temp_income_account_id.id,
                                                  'name':'/'
                                                  }),
                                            (0,0,{
                                                  'credit':amount_accrued,
                                                  'account_id':self.account_id.id,
                                                  'name':'Accrual of %s'%origin_id.display_name
                                                  })
                                            
                                            
                                            ]
                                
                                })
                if self.post:
                    move_id.action_post()
            if origin_id:
                origin_id.account_move_ids = [(4,move_id.id)] 
            
        
        
        