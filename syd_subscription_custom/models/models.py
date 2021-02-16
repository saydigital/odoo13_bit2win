# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    subscription_start_date = fields.Date(readonly=False)
    subscription_end_date = fields.Date(readonly=False)