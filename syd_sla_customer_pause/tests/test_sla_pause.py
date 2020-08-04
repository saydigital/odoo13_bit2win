# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import UserError, AccessError, ValidationError

class TestHelpdeskTicket(TransactionCase):

    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()

        self.HelpdeskSlaTicket_id = self.env['helpdesk.ticket'].create({
            'name':'Test SLA da codice'})

        self.awaitingStage = self.env['helpdesk.stage'].create({
            'name':'Awaiting', 
            'sequence': 1, 
            'is_close': False, 
            'fold':True })
    
    #COMPUTE_REMAINING_SLA_DAYS
    def test_sum_oneWeekAwaiting_compute(self):
        # arrange
        days_for_sla_completion = 14
        time_creation_ticket = fields.Datetime.now().replace(day=1, month=7, year=2020, hour=12, minute=0, second=0)
        time_start_awaiting = fields.Datetime.now().replace(day=10, month=7, year=2020, hour=12, minute=0, second=0)
        #time_end_awaiting = fields.Datetime.now().replace(day=15, month=7, year=2020, hour=12, minute=0, second=0)
        time_now = fields.Datetime.now().replace(day=17, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        remaining_days = self.HelpdeskSlaTicket_id.compute_remainig_sla_days(days_for_sla_completion, time_now-time_creation_ticket, time_now-time_start_awaiting )
    
        # assert
        self.assertEqual(remaining_days,5)

    #COMPUTE_ELAPSED_TIME_FROM_TICKET_CREATION
    def test_difference_sameMonthsDifferentDays_compute(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=1, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket_id.compute_elapsed_time_from_ticket_creation(date_creation_ticket, time_end_awaiting)
        
        # assert 
        self.assertEqual(time_from_ticket_creation.days, 13)
        self.assertEqual(time_from_ticket_creation.seconds, 0)
        
    def test_difference_monthsYearDaysDifferent_compute(self):
        # arrange
        date_creation_ticket = fields.Datetime.now().replace(day=10, month=7, year=2020, hour=20, minute=0, second=4)
        time_end_awaiting = fields.Datetime.now().replace(day=24, month=7, year=2020, hour=20, minute=0, second=7)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket_id.compute_elapsed_time_from_ticket_creation(date_creation_ticket, time_end_awaiting)
        
        # assert 
        self.assertEqual(time_from_ticket_creation.days, 10)
        self.assertEqual(time_from_ticket_creation.seconds, 0)
        
    def test_difference_monthsYearDaysDifferentChristmasHoliday_compute(self):
        # arrange
        date_creation_ticket = fields.Datetime.now().replace(day=23, month=12, year=2020, hour=20, minute=0, second=0)
        time_end_awaiting = fields.Datetime.now().replace(day=28, month=12, year=2020, hour=20, minute=0, second=0)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket_id.compute_elapsed_time_from_ticket_creation(date_creation_ticket, time_end_awaiting)
        
        # assert 
        self.assertEqual(time_from_ticket_creation.days, 3)
        self.assertEqual(time_from_ticket_creation.seconds, 0)
    
    def test_difference_daysTheSame_compute(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        
        # act
        time_from_ticket_creation = self.HelpdeskSlaTicket_id.compute_elapsed_time_from_ticket_creation(date_creation_ticket, time_end_awaiting) 

        # assert 
        self.assertEqual(time_from_ticket_creation.days, 0)
        self.assertEqual(time_from_ticket_creation.seconds, 0)
        
    def test_difference_daysNegative_exception(self):
        # arrange
        time_end_awaiting = fields.Datetime.now().replace(day=20, month=7, year=2020, hour=12, minute=0, second=0)
        date_creation_ticket = fields.Datetime.now().replace(day=10, month=7, year=2020, hour=12, minute=0, second=0)
        
        # assert
        with self.assertRaises(ValidationError):
            # act
            self.HelpdeskSlaTicket_id.compute_elapsed_time_from_ticket_creation(time_end_awaiting, date_creation_ticket)

    #COMPUTE_DEADLINE
    def test_calculation_deadlineOneMonthJuly_compute(self):
        # arrange
        time_now = fields.Datetime.now().replace(day=31, month=7, year=2020, hour=12, minute=0, second=0)
        deadline = fields.Datetime.now().replace(day=31, month=7, year=2020, hour=16, minute=0, second=0)
        
        # act
        remaining_days = 0
                            
        final_deadline = self.HelpdeskSlaTicket_id.compute_deadline(self.env['resource.calendar'].search([('id','=','1')]), remaining_days, deadline, time_now, 0)
        
        self.assertEqual(final_deadline.day, 31)