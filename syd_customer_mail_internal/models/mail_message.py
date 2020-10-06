# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, modules, tools

class Message(models.Model):
    _inherit = 'mail.message'
 
    @api.model
    def _get_default_from(self):
        if self.env.user.email:
            if self.env.user.partner_ids[0].email_internal:
                return tools.formataddr((self.env.user.name, self.env.user.partner_ids[0].email_internal))
            return tools.formataddr((self.env.user.name, self.env.user.email))
        raise UserError(_("Unable to post message, please configure the sender's email address."))
