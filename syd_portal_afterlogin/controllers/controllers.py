# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.web.controllers.main import ensure_db, Home
    
class Website(Home):

    @http.route(website=True, auth="public", sitemap=False)
    def web_login(self, redirect=None, *args, **kw):
        response = super(Website, self).web_login(redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            
            if request.session.uid and not request.params.get('redirect') and request.website.url_afterlogin: 
                redirect = request.website.url_afterlogin           
            
            elif request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                redirect = '/my'
                
            return http.redirect_with_hash(redirect)
        return response
