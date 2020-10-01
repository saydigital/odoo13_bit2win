# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class Page(models.Model):
#    _inherit = 'website.page'
    
#    url_logged = fields.Char('Page URL Logged')

    
class Menu(models.Model):

    _inherit = "website.menu"
    
    url_logged = fields.Char('Page URL Logged')
