from odoo import api, fields, models, _
from odoo import exceptions 
from datetime import datetime, timedelta

class HelpdeskTicket(models.Model):
    _inherit = ["helpdesk.ticket"]
    _description = 'Helpdesk ticket inherit'
    
    awaiting_start = fields.Datetime()
    
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *,
                     body='', subject=None, message_type='notification',
                     email_from=None, author_id=None, parent_id=False,
                     subtype_id=False, subtype=None, partner_ids=None, channel_ids=None,
                     attachments=None, attachment_ids=None,
                     add_sign=True, record_name=False,
                     **kwargs):
        
        message =  super(HelpdeskTicket, self).message_post(body=body, subject=subject, message_type=message_type,
                     email_from=email_from, author_id=author_id, parent_id=parent_id,
                     subtype_id=subtype_id, subtype=subtype, partner_ids=partner_ids, channel_ids=channel_ids,
                     attachments=attachments, attachment_ids=attachment_ids,
                     add_sign=add_sign, record_name=record_name,
                     **kwargs)
            
        communication_user_id = self.team_id.communication_user_id  
        
        if bool(communication_user_id) & bool(1 in self.env.user.groups_id.ids):
            message.communication_user_id = communication_user_id.id
            
        return message    
   
    def write(self, vals):
        
        if self._is_awaiting_state(vals.get('stage_id')):
            vals['awaiting_start'] = fields.Datetime.now()
        elif self._is_prev_state_awaiting():
            self.recompute_sla_after_waiting()
            
            vals['awaiting_start'] = None
        
        super(HelpdeskTicket, self).write(vals)
        
    def recompute_sla_after_waiting(self):
        datetime_now = fields.Datetime.now() 
        
        for status in self.sla_status_ids:

            # If SLA closed break this iteration            
            if status.reached_datetime != False:
                continue
            
            working_calendar = status.ticket_id.team_id.resource_calendar_id

            if not working_calendar:
                status.deadline = deadline
                continue
            
            sla_time_days = status.sla_id.time_days + 1
            elapsed_time_from_ticket_cration = self.compute_elapsed_time_from_ticket_creation(status.ticket_id.create_date, datetime_now)
            elapsed_time_in_awaiting_state = datetime_now - status.ticket_id.awaiting_start
            
            remainig_sla_days = self.compute_remainig_sla_days(
                                        sla_time_days,
                                        elapsed_time_from_ticket_cration,
                                        elapsed_time_in_awaiting_state)            

            if status.sla_id.time_days > 0:
                status.sudo().deadline = self.compute_deadline(working_calendar, remainig_sla_days, datetime_now, datetime_now, status.sla_id.time_hours)

    def compute_remainig_sla_days(self, days_for_sla_completion, elapsed_time_from_ticket_cration, awaiting_time):
        
        return (timedelta(days=days_for_sla_completion) - elapsed_time_from_ticket_cration + awaiting_time).days
    
    def compute_elapsed_time_from_ticket_creation(self, ticket_create_date, time_now):
        if(time_now < ticket_create_date):
            raise exceptions.ValidationError('The ticket creation date cannot be after than now')
        
        work_days = self.team_id.resource_calendar_id.get_work_duration_data(ticket_create_date, time_now, compute_leaves=True)
        
        return timedelta(days=int(work_days['days']))
        
    def compute_deadline(self, working_calendar, remainig_sla_days, deadline, create_dt, time_hours):
        new_deadline = working_calendar.plan_days(remainig_sla_days, deadline, compute_leaves=True)
                
        #new_deadline = new_deadline.replace(hour=deadline.hour, minute=deadline.minute, second=deadline.second, microsecond=deadline.microsecond)
        
        return new_deadline
        #return self.compute_plan_hours(working_calendar, time_hours, new_deadline)
    
    def compute_plan_hours(self, working_calendar, time_hours, deadline):
        return working_calendar.plan_hours(time_hours, deadline, compute_leaves=True)

    # Utilities
    def _is_prev_state_awaiting(self):
        return self._is_awaiting_state(self.stage_id.id)
    
    def _is_awaiting_state(self, stage_id):
        AWAITING_STATE = "awaiting"

        stage_id = self.env['helpdesk.stage'].browse(stage_id)
        
        if stage_id.id == False: 
            return False
        
        return (AWAITING_STATE in stage_id.name.lower())