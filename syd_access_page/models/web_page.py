# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.http import request
import werkzeug.utils

class Website(models.Model):
    _inherit = "website"
    
    url_authenticated = fields.Char('Page not authenticated users')
    pages_authenticated_by_page = fields.Boolean('Pages authenticated Default')
            
class Page(models.Model):
    _inherit = "website.page"
    
    authenticated_page = fields.Boolean('Authentication Page')
        
    @api.onchange('website_id')
    @api.constrains('website_id')
    def onchange_validate_order(self):
        self.authenticated_page = self.website_id.pages_authenticated_by_page

class Http(models.AbstractModel):
    _inherit = 'ir.http'
    
    @classmethod
    def _serve_page(cls):
        page = super(Http, cls)._serve_page()
            
        page_domain = [('url', '=', request.httprequest.path)] + request.website.website_domain()
        page_searched = request.env['website.page'].sudo().search(page_domain, order='website_id asc', limit=1)
        
        # If page not found or user is authenticated, follow the standard flow 
        if(page == False or request.session.uid != None 
             or request.httprequest.path == request.website.url_authenticated
             or request.httprequest.path == "/" 
             or page_searched.authenticated_page == False
             or request.website.url_authenticated == False):
            return page
        
        return werkzeug.utils.redirect(request.website.url_authenticated)