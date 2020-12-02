# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Contract(models.Model):
    _inherit = 'hr.contract'
    
    has_daily_ticket_restaurant = fields.Boolean('Daily ticket restaurant?')