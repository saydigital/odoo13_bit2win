# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
import uuid

class ResCompany(models.Model):
    _inherit = "res.company"
    
    company_hash = fields.Char('Company Hash',default=lambda self: self._generate_company_hash()) 
    
    @api.model
    def _generate_company_hash(self):
        return str(uuid.uuid4())

    
    