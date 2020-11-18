# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.http import request
import werkzeug.utils

class Website(models.Model):
    _inherit = "website"
    
    url_authenticated = fields.Char('Page not auth')
    pages_authenticated_by_page = fields.Boolean('Pages authenticated By Default', compute='_compute_visible')

    def _compute_visible(self):
        for page in self:
            page.is_visible = page.website_published and (
                not page.date_publish or page.date_publish < fields.Datetime.now()
            )
            
class Page(models.Model):
    _inherit = "website.page"
    
    authenticated_page = fields.Boolean('Authentication Page')

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
             or page_searched.authenticated_page == False):
            return page
        
        return werkzeug.utils.redirect(request.website.url_authenticated)