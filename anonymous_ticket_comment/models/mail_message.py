# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Message(models.Model):
    _inherit = 'mail.message'
 
    communication_user_id = fields.Many2one('res.partner', 'Author')
    
    def portal_message_format(self):
        return self._portal_message_format([
            'id', 'body', 'date', 'author_id', 'email_from',  # base message fields
            'message_type', 'subtype_id', 'subject',  # message specific
            'model', 'res_id', 'record_name',  # document related
            'communication_user_id'
        ])
