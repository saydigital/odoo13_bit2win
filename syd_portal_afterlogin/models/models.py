# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class Page(models.Model):
#    _inherit = 'website.page'
    
#    url_logged = fields.Char('Page URL Logged')

    
class Website(models.Model):

    _inherit = "website"
    
    url_afterlogin = fields.Char('Page URL After Login')
