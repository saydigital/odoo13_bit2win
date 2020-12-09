# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    
    swift_code_1 = fields.Char('Swift Code 1')
    swift_code_2 = fields.Char('Swift Code 2')
    iban = fields.Char('IBAN')
    account_name_custom = fields.Char('Account Name')