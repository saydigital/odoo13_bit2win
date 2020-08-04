# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"
    
    communication_user_id = fields.Many2one('res.partner', 'Author')
    
class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *,
                     body='', subject=None, message_type='notification',
                     email_from=None, author_id=None, parent_id=False,
                     subtype_id=False, subtype=None, partner_ids=None, channel_ids=None,
                     attachments=None, attachment_ids=None,
                     add_sign=True, record_name=False,
                     **kwargs):
        
        if self._is_user_from_backend() & bool(message_type=='comment') & bool(subtype=='mail.mt_comment'):
            author_id = self.team_id.communication_user_id.id #invert user
        
        message = super(HelpdeskTicket, self).message_post(body=body, subject=subject, message_type=message_type,
                     email_from=email_from, author_id=author_id, parent_id=parent_id,
                     subtype_id=subtype_id, subtype=subtype, partner_ids=partner_ids, channel_ids=channel_ids,
                     attachments=attachments, attachment_ids=attachment_ids,
                     add_sign=add_sign, record_name=record_name,
                     **kwargs)
        
        if self._is_user_from_backend() & bool(message_type=='comment') & bool(subtype=='mail.mt_comment'):
            message.communication_user_id = self.env.user.partner_id
            
            #Log the message
            self._log_note_message(body=body, subject=subject, message_type=message_type,
                     email_from=email_from, author_id=author_id, parent_id=parent_id,
                     subtype_id=subtype_id, subtype=subtype, partner_ids=partner_ids, channel_ids=channel_ids,
                     attachments=attachments, attachment_ids=attachment_ids,
                     add_sign=add_sign, record_name=record_name,
                     **kwargs)
            
        return message
    
    def _is_user_from_backend(self):
        #if 1 user is from backend
        return (bool( self.team_id.communication_user_id) & bool(1 in self.env.user.groups_id.ids))
    
    def _log_note_message(self,body='', subject=None, message_type='notification',
                     email_from=None, author_id=None, parent_id=False,
                     subtype_id=False, subtype=None, partner_ids=None, channel_ids=None,
                     attachments=None, attachment_ids=None,
                     add_sign=True, record_name=False,
                     **kwargs):
            
            subtype = 'mail.mt_note'
            body = 'Message sent by: ' + str(self.env.user.partner_id.name)
            author_id = self.env.user.partner_id.id
            
            super(HelpdeskTicket, self).message_post(body=body, subject=subject, message_type=message_type,
                     email_from=email_from, author_id=author_id, parent_id=parent_id,
                     subtype_id=subtype_id, subtype=subtype, partner_ids=partner_ids, channel_ids=channel_ids,
                     attachments=attachments, attachment_ids=attachment_ids,
                     add_sign=add_sign, record_name=record_name,
                     **kwargs)