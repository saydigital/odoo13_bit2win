# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import inspect
import re
import os


class MailCheckLog(models.Model):
    _name = "syd_check_businessmail.refused_email"
    
    date_attempt = fields.Datetime('Date Insert Domain', default=fields.Datetime.now)
    domain_failed = fields.Char('Domain refused')