# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo import fields

class TestHelpdeskTicket(TransactionCase):
    
    
    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()

        self.HelpdeskSlaTicket = self.env['helpdesk.ticket'].create({
            'name':'Test SLA da codice'})

        self.awaitingStage = self.env['helpdesk.stage'].create({
            'name':'Awaiting', 
            'sequence': 1, 
            'is_close': False, 
            'fold':True })
    
    
    
    #COMPUTE_REMAINING_SLA_DAYS
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


    #COMPUTE_ELAPSED_TIME_FROM_TICKET_CREATION
    def test_Difference_SameMonthsDifferentDays_compute(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=1, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket.compute_elapsed_time_from_ticket_creation(date_creation_ticket, time_end_awaiting)
        
        # assert 
        self.assertEqual(time_from_ticket_creation.days, 19)
        self.assertEqual(time_from_ticket_creation.seconds, 0)
        
    def test_Difference_MonthsYearDaysDifferent_compute(self):
        # arrange
        date_creation_ticket = fields.Datetime.now().replace(day=1, month=7, year=2020, hour=20, minute=0, second=4)
        time_end_awaiting = fields.Datetime.now().replace(day=31, month=7, year=2020, hour=20, minute=0, second=7)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket.compute_elapsed_time_from_ticket_creation(date_creation_ticket, time_end_awaiting)
        
        # assert 
        self.assertEqual(time_from_ticket_creation.days, 23)
        self.assertEqual(time_from_ticket_creation.seconds, 74823)
    
    def test_Difference_DaysTheSame_compute(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket.compute_elapsed_time_from_ticket_creation(date_creation_ticket, time_end_awaiting) 

        # assert 
        self.assertEqual(time_from_ticket_creation.days, 0)
        self.assertEqual(time_from_ticket_creation.seconds, 0)
        
    def test_Difference_DaysNegative_exception(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=10, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        #self.assertRaises(self.HelpdeskSlaTicket.compute_elapsed_time_from_ticket_creation(time_end_awaiting, date_creation_ticket))

        # assert 
        #self.assertException(time_from_ticket_creation)
        
        
        
        
        
        
        
        
        
        
        
    def test_work_duration(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=26, month=12, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=25, month=12, year=2020, hour=12, minute=0, second=0)
        
        
        calendar_id = self.env['resource.calendar'].browse(1)
        
        work_duration = calendar_id.get_work_duration_data(date_creation_ticket, time_end_awaiting, compute_leaves=True)
        
        a = 0
        
        #duration_data = status.ticket_id.team_id.resource_calendar_id.get_work_duration_data(start_dt, end_dt, compute_leaves=True)

               