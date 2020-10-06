# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError



class ResPartner(models.Model):
    _inherit = "res.partner"
    
    email_internal = fields.Char('Internal Email for Customer')

    
