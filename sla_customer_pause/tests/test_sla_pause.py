# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo import fields

class TestHelpdeskTicket(TransactionCase):
    
    
    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()

        self.HelpdeskSlaTicket = self.env['helpdesk.ticket']

        self.awaitingStage = self.env['helpdesk.stage'].create({'name':'Awaiting', 'sequence': 1, 'is_close': False, 'fold':True })
    
    
    def test_Sum_OneWeekAwaiting_compute(self):
        # arrange
        days_for_sla_completion = 14
        time_creation_ticket = fields.Datetime.now().replace(day=1, month=7, year=2020, hour=12, minute=0, second=0)
        time_start_awaiting = fields.Datetime.now().replace(day=10, month=7, year=2020, hour=12, minute=0, second=0)
        #time_end_awaiting = fields.Datetime.now().replace(day=15, month=7, year=2020, hour=12, minute=0, second=0)
        time_now = fields.Datetime.now().replace(day=17, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        remaining_days = self.HelpdeskSlaTicket.compute_remainig_sla_days(days_for_sla_completion, time_now-time_creation_ticket, time_now-time_start_awaiting )
    
        # assert
        self.assertEqual(remaining_days,5)
    
    def test_Difference_SameMonthsDifferentDays_compute(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=1, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket.compute_elapsed_time_from_ticket_cration(date_creation_ticket, time_end_awaiting)
        
        # assert 
        self.assertEqual(time_from_ticket_creation.days, 19)
        self.assertEqual(time_from_ticket_creation.seconds, 0)
        
    def test_Difference_MonthsYearDaysDifferent_compute(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=21, month=7, year=2020, hour=17, minute=37, second=7)
        date_creation_ticket = fields.Datetime.now().replace(day=1, month=6, year=2018, hour=20, minute=50, second=4)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket.compute_elapsed_time_from_ticket_cration(date_creation_ticket, time_end_awaiting)
        
        # assert 
        self.assertEqual(time_from_ticket_creation.days, 780)
        self.assertEqual(time_from_ticket_creation.seconds, 74823)
    
    def test_Difference_DaysTheSame_compute(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket.compute_elapsed_time_from_ticket_cration(date_creation_ticket, time_end_awaiting) 

        # assert 
        self.assertEqual(time_from_ticket_creation.days, 0)
        self.assertEqual(time_from_ticket_creation.seconds, 0)
        
    def test_Difference_DaysNegative_exception(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=10, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        #self.assertRaises(self.HelpdeskSlaTicket.compute_elapsed_time_from_ticket_cration(time_end_awaiting, date_creation_ticket))

        # assert 
        #self.assertException(time_from_ticket_creation)
               