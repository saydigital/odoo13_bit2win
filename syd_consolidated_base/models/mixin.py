# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
import xmlrpc.client

class Alignable(models.AbstractModel):
    _name = "consolidated.align_mixin"
    _description = 'Description'
    

    external_id = fields.Integer('External Id')
    last_updated_date = fields.Datetime('Last Updated Date')
    instance_id = fields.Many2one('consolidated.instance',string="Instance")

    

    
    
    
    