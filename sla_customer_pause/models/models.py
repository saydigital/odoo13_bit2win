# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import exceptions 

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"
    _description = 'Helpdesk ticket inherit'
    
    awaiting_start = fields.Datetime()

    def write(self, vals):
        
        if self._is_awaiting_state(vals.get('stage_id')):
            vals['awaiting_start'] = fields.Datetime.now()
        elif self._is_prev_state_awaiting():
            self._recompute_sla_after_waiting()
            
            
            vals['awaiting_start'] = None
        
        super(HelpdeskTicket, self).write(vals)
        
    def recompute_sla_after_waiting(self):
        datetime_now = fields.Datetime.now() 
        
        for status in self.sla_status_ids:

            #If SLA closed break this iteration            
            if status.reached_datetime != False:
                continue
            
            working_calendar = status.ticket_id.team_id.resource_calendar_id

            if not working_calendar:
                status.deadline = deadline
                continue

            remainig_sla_days = self.compute_remainig_sla_days(
                                        (status.sla_id.time_days + 1), 
                                        self.compute_elapsed_time_from_ticket_cration(status.ticket_id.create_date, datetime_now), 
                                        (datetime_now - status.ticket_id.awaiting_start ))            

            if status.sla_id.time_days > 0:
                status.sudo().deadline = self.compute_deadline(working_calendar, remainig_sla_days, datetime_now, datetime_now, status.sla_id.time_hours)

    #To-Do: il calcolo dei giorni di SLA rimanenti deve tenere conto dei giorni festivi? 
    def compute_remainig_sla_days(self, days_for_sla_completion, elapsed_time_from_ticket_cration, awaiting_time ):
        return (days_for_sla_completion - elapsed_time_from_ticket_cration.days + awaiting_time.days)
    
    def compute_elapsed_time_from_ticket_cration(self, ticket_create_date, time_now):
        if(time_now < ticket_create_date):
            raise exceptions.ValidationError('The ticket creation date cannot be after than now')
        
        return time_now - ticket_create_date
    
    def compute_deadline(self, working_calendar, remainig_sla_days, deadline, create_dt, time_hours):
        deadline = working_calendar.plan_days(remainig_sla_days, deadline, compute_leaves=True)
                
        deadline.replace(hour=create_dt.hour, minute=create_dt.minute, second=create_dt.second, microsecond=create_dt.microsecond)
    
        return self.compute_plan_hours(time_hours,deadline)
    
    def compute_plan_hours(self, time_hours, deadline):
        return working_calendar.plan_hours(time_hours, deadline, compute_leaves=True)
    

    #Utilities
    def _is_prev_state_awaiting(self):
        return self._is_awaiting_state(self.stage_id.id)
    
    def _is_awaiting_state(self, stage_id):
        AWAITING_STATE = "awaiting"

        stage_id = self.env['helpdesk.stage'].browse(stage_id)
        
        if stage_id.id == False: 
            return False
        
        return (self.AWAITING_STATE in stage_id.name.lower())
