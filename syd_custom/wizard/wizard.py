# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError



class Wizard(models.TransientModel):
    _name="syd_custom.wizard_fix"
    
    date_fix =  fields.Date('Planned Fix Date',required=True)
    ticket_id = fields.Many2one('helpdesk.ticket',string="Ticket")
    
    
    def set_fix(self):
        self.ticket_id.write({
                              'date_fix':self.date_fix,
                              'fixing':True
                              })
    
    
    
    
