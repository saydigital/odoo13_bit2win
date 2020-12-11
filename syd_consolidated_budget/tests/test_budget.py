# -*- coding: utf-8 -*-
# © 2019 SayDigital s.r.l.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase
import datetime
from odoo.fields import Date
from unittest.mock import patch
from odoo.exceptions import UserError, AccessError, ValidationError

class TestSydConsolidatedCommon(SavepointCase):

    @classmethod
    def setUpClass(self):
        super(TestAccountSydBudgetCommon, self).setUpClass()
        
        self.project_1 = self.env['project.project'].create({
            'name': 'Project',
            'allow_timesheets':True
            })
        self.account_budget_timesheet = self.env['account.budget.post'].create({
            'name': 'Timesheet Position',
            'type':'timesheet'
        })
        self.account_budget_matured = self.env['account.budget.post'].create({
            'name': 'Matured Position',
            'type':'matured'
        })
        self.account_budget_parent = self.env['account.budget.post'].create({
            'name': 'Parent Position',
            'type':'parent'
        })
        self.account_budget_general = self.env['account.budget.post'].create({
            'name': 'General Position',
            'type':'general'
        })
        self.budget_project = self.env['crossovered.budget'].create({
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year)),
            'date_to': Date.from_string('%s-12-31' % (datetime.datetime.now().year)),
            'name': 'Budget %s' % (datetime.datetime.now().year + 1),
            'state': 'draft',
            'analytic_account_id':self.project_1.analytic_account_id.id
        })
        self.line1 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project.id,
            'analytic_account_id': self.project_1.analytic_account_id.id,
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year )),
            'date_to': Date.from_string('%s-01-31' % (datetime.datetime.now().year )),
            'general_budget_id': self.account_budget_timesheet.id,
            'planned_amount': -800.0,
        })
        self.line2 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project.id,
            'analytic_account_id': self.project_1.analytic_account_id.id,
            'date_from': Date.from_string('%s-02-01' % (datetime.datetime.now().year )),
            'date_to': Date.from_string('%s-02-28' % (datetime.datetime.now().year )),
            'general_budget_id': self.account_budget_matured.id,
            'planned_amount': 40.0,
        })
        
        self.line3 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project.id,
            'analytic_account_id': self.project_1.analytic_account_id.id,
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year )),
            'date_to': Date.from_string('%s-02-28' % (datetime.datetime.now().year )),
            'general_budget_id': self.account_budget_parent.id,
            'planned_amount': 2000.0,
        })
        
        self.partner_1 = self.env['res.partner'].create({
            'name': 'My User'
        })
        self.user_1 = self.env['res.users'].create({
            'login': 'My User',
            'company_id':  self.env.ref('base.main_company').id,
            'company_ids': [(4,  self.env.ref('base.main_company').id)],
            'partner_id': self.partner_1.id,
        })
        self.employee_1 = self.env['hr.employee'].create({
            'user_id':self.user_1.id,
            'timesheet_cost':100.0
            })
        
        
    def test_timesheet_budget(self):
        self.al1 = self.env['account.analytic.line'].create(
                        {        
                         'user_id':self.user_1.id,
                         'project_id':self.project_1.id,
                         'employee_id':self.employee_1.id,
                         'account_id':self.project_1.analytic_account_id.id,
                         'unit_amount':8,
                         'date':Date.from_string('%s-01-20' % (datetime.datetime.now().year )),
                        })
        self.al1.flush()
        self.assertEqual(self.line1.practical_amount, -800.0)
    
    
    def test_budget_matured(self):
        def patched_today(*args, **kwargs):
            return Date.from_string('%s-03-01' % (datetime.datetime.now().year))
        self.line2.matured_amount = 900
        with patch('odoo.fields.Date.today', patched_today):
            self.assertEqual(self.line2.practical_amount, 900.0)
     
    def test_budget_confirm(self):
#         with self.assertRaises(ValidationError):
#             self.budget_project.action_budget_confirm()
        self.line4 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project.id,
            'analytic_account_id': self.project_1.analytic_account_id.id,
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year)),
            'date_to': Date.from_string('%s-12-31' % (datetime.datetime.now().year)),
            'general_budget_id': self.account_budget_general.id,
            'planned_amount':0.0,
        })
        self.budget_project2 = self.env['crossovered.budget'].create({
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year)),
            'date_to': Date.from_string('%s-12-31' % (datetime.datetime.now().year)),
            'name': 'Budget %s' % (datetime.datetime.now().year + 1),
            'state': 'draft',
            'analytic_account_id':self.project_1.analytic_account_id.id
        })
        with self.assertRaises(ValidationError):
            self.budget_project.action_budget_confirm()
        
        self.line5 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project.id,
            'analytic_account_id': False,
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year)),
            'date_to': Date.from_string('%s-12-31' % (datetime.datetime.now().year)),
            'general_budget_id': self.account_budget_general.id,
            'planned_amount':0.0,
        })
        with self.assertRaises(ValidationError):
            self.budget_project.action_budget_confirm()
        self.budget_project2.unlink()
        self.line5.unlink()
        self.budget_project.action_budget_confirm()
        self.assertEqual(self.budget_project.state, 'confirm')
        
            
    def test_budget_parent(self):
        def patched_today(*args, **kwargs):
            return Date.from_string('%s-03-01' % (datetime.datetime.now().year))
        self.al1 = self.env['account.analytic.line'].create(
                        {        
                         'user_id':self.user_1.id,
                         'project_id':self.project_1.id,
                         'employee_id':self.employee_1.id,
                         'account_id':self.project_1.analytic_account_id.id,
                         'unit_amount':8,
                         'date':Date.from_string('%s-01-20' % (datetime.datetime.now().year )),
                        })
        self.al1.flush()
        self.line2.matured_amount = 900
        self.budget_project.action_budget_validate()
        with patch('odoo.fields.Date.today', patched_today):
            self.assertEqual(self.line3.practical_amount, 100.0) # 900-800
        
    def test_details(self):
        self.env['crossovered.budget.line_planned_details'].create({
                                                                    'crossovered_budget_line_id':self.line2.id,
                                                                    'price_unit':50,
                                                                    'qty':10,
                                                                    'name':'Function Point'
                                                                   })
        self.env['crossovered.budget.line_planned_details'].create({
                                                                    'crossovered_budget_line_id':self.line2.id,
                                                                    'price_unit':20,
                                                                    'qty':10,
                                                                    'name':'T&M'
                                                                   })
        self.assertEqual(self.line2.planned_amount, 700.0)
        self.assertEqual(len(self.line2.matured_details), 0)
        self.budget_project.action_budget_validate()
        self.assertEqual(len(self.line2.matured_details), 2)
        
    def test_wizard_helper(self):
        self.budget_project_2 = self.env['crossovered.budget'].create({
            'date_from': Date.from_string('2018-01-05'),
            'date_to': Date.from_string('2018-02-09'),
            'name': 'Budget %s' % (datetime.datetime.now().year + 1),
            'state': 'draft',
            'analytic_account_id':self.project_1.analytic_account_id.id
        })
        self.assertEqual(len(self.budget_project_2.crossovered_budget_line), 0)
        wizard = self.env['syd_budget_extended.budget_helper'].create({
                                                                           'crossovered_budget_id':self.budget_project_2.id,
                                                                           'general_budget_id':self.account_budget_timesheet.id,
                                                                           'date_from':self.budget_project_2.date_from,
                                                                           'date_to':self.budget_project_2.date_to,
                                                                           'type':'month'
                                                                           })
        wizard.generate_lines()
        self.assertEqual(len(self.budget_project_2.crossovered_budget_line), 2)
        line1 = self.env['crossovered.budget.lines'].search([('crossovered_budget_id','=',self.budget_project_2.id)], order='date_from asc',limit=1)
        self.assertEqual(line1.date_from,Date.from_string('2018-01-05'))
        self.assertEqual(line1.date_to,Date.from_string('2018-01-31'))
        line1 = self.env['crossovered.budget.lines'].search([('crossovered_budget_id','=',self.budget_project_2.id)], order='date_from desc',limit=1)
        self.assertEqual(line1.date_from,Date.from_string('2018-02-01'))
        self.assertEqual(line1.date_to,Date.from_string('2018-02-09'))
        
    
    def test_budget_activities(self):
        def patched_today(*args, **kwargs):
            return Date.from_string('%s-03-01' % (datetime.datetime.now().year))
        self.assertEqual(len(self.budget_project.activity_ids), 0)
        self.line4 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project.id,
            'analytic_account_id': self.project_1.analytic_account_id.id,
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year)),
            'date_to': Date.from_string('%s-12-31' % (datetime.datetime.now().year)),
            'general_budget_id': self.account_budget_general.id,
            'planned_amount':0.0,
        })
        with patch('odoo.fields.Date.today', patched_today):
            self.budget_project.action_budget_confirm()
            self.assertEqual(len(self.budget_project.activity_ids), 1)
            self.budget_project.action_budget_validate()
            self.assertEqual(len(self.budget_project.activity_ids), 0)
            # Test Matured
            self.env['crossovered.budget']._activity_matured()
            self.assertEqual(len(self.budget_project.activity_ids), 1)
            self.line2.matured_amount = 100.0
            self.assertEqual(len(self.budget_project.activity_ids), 0)
            self.budget_project.action_budget_confirm()
            self.assertEqual(len(self.budget_project.activity_ids), 1)
            self.budget_project.action_budget_cancel()
            self.assertEqual(len(self.budget_project.activity_ids), 0)
        
    def test_margin(self):
        
        
        self.budget_project_margin = self.env['crossovered.budget'].create({
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year)),
            'date_to': Date.from_string('%s-12-31' % (datetime.datetime.now().year)),
            'name': 'Budget %s' % (datetime.datetime.now().year + 1),
            'state': 'draft',
            'analytic_account_id':self.project_1.analytic_account_id.id
        })
        self.line_m_1 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project_margin.id,
            'analytic_account_id': self.project_1.analytic_account_id.id,
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year )),
            'date_to': Date.from_string('%s-01-31' % (datetime.datetime.now().year )),
            'general_budget_id': self.account_budget_timesheet.id,
            'planned_amount': -800.0,
        })
        self.line_m_2 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project_margin.id,
            'analytic_account_id': self.project_1.analytic_account_id.id,
            'date_from': Date.from_string('%s-02-01' % (datetime.datetime.now().year )),
            'date_to': Date.from_string('%s-02-28' % (datetime.datetime.now().year )),
            'general_budget_id': self.account_budget_timesheet.id,
            'planned_amount': -400.0,
        })
        
        self.line_m_3 = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': self.budget_project_margin.id,
            'analytic_account_id': self.project_1.analytic_account_id.id,
            'date_from': Date.from_string('%s-01-01' % (datetime.datetime.now().year )),
            'date_to': Date.from_string('%s-02-28' % (datetime.datetime.now().year )),
            'general_budget_id': self.account_budget_matured.id,
            'planned_amount': 2000.0,
        })
        self.assertEquals(self.budget_project_margin.planned_margin,0.4)
   