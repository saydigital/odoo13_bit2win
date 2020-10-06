# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, modules, tools

class Message(models.Model):
    _inherit = 'mail.message'
    
   
    @api.model
    def _is_user_from_frontend(self):
        # if 1 user is from backend
        return (bool(8 in self.env.user.groups_id.ids))

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
           if self._is_user_from_frontend() and self.env.user.company_id.email_internal:
            values['email_from'] =  tools.formataddr((self.env.user.name, self.env.user.company_id.email_internal))
        return super(Message, self).create(values_list)