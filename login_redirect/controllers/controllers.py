# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import WebClient, Home
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class Website(Home):
    
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        
        # TODO: Check if user is Portal!!
        if(request.session.uid != None):  # User Auth
            homepage = request.website.menu_id.url_logged 
            
            if homepage and request.env.user.has_group('base.group_user') and homepage != '/':
                return request.env['ir.http'].reroute(homepage)
        # End custom fix 
        
        homepage = request.website.homepage_id
        if homepage and (homepage.sudo().is_visible or request.env.user.has_group('base.group_user')) and homepage.url != '/':
            return request.env['ir.http'].reroute(homepage.url)

        website_page = request.env['ir.http']._serve_page()
        if website_page:
            return website_page
        else:
            top_menu = request.website.menu_id
            first_menu = top_menu and top_menu.child_id and top_menu.child_id.filtered(lambda menu: menu.is_visible)
            if first_menu and first_menu[0].url not in ('/', '', '#') and (not (first_menu[0].url.startswith(('/?', '/#', ' ')))):
                return request.redirect(first_menu[0].url)

        raise request.not_found()
