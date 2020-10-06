# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError



class ResCompany(models.Model):
    _inherit = "res.company"
    
    email_internal = fields.Char('Internal Email for Customer')

    
