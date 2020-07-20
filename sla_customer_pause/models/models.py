# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

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
        
    #Utilities
    def _recompute_sla_after_waiting(self):
        for status in self.sla_status_ids:

            #If SLA closed break this iteration            
            if status.reached_datetime != False:
                continue
            
            deadline = fields.Datetime.now()
            create_dt = fields.Datetime.now()
            
            working_calendar = status.ticket_id.team_id.resource_calendar_id

            if not working_calendar:
                status.deadline = deadline
                continue


                
            days_for_sla_completion = status.sla_id.time_days + 1
            elapsed_time_from_ticket_cration = fields.Datetime.now() - status.ticket_id.create_date
            


            remainig_sla_days = days_for_sla_completion - elapsed_time_from_ticket_cration.days + (fields.Datetime.now() - status.ticket_id.awaiting_start ).days                   

            if status.sla_id.time_days > 0:
                deadline = working_calendar.plan_days(remainig_sla_days, deadline, compute_leaves=True)
                
                #Allineo la scadenza del ticket all'orario di adesso
                deadline = deadline.replace(hour=create_dt.hour, minute=create_dt.minute, second=create_dt.second, microsecond=create_dt.microsecond)

            status.sudo().deadline = working_calendar.plan_hours(status.sla_id.time_hours, deadline, compute_leaves=True)

    
    def _is_prev_state_awaiting(self):
        return self._is_awaiting_state(self.stage_id.id)
    
    def _is_awaiting_state(self, stage_id):
        AWAITING_STATE = "awaiting"

        stage_id = self.env['helpdesk.stage'].browse(stage_id)
        
        if stage_id.id == False: 
            return False
        
        return (self.AWAITING_STATE in stage_id.name.lower())