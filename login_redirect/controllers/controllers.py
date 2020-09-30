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
        
        
        #NOT WORKING!
        if(request.session.uid != None): #Auth user TO-DO user from Support? 
            homepage = request.env['website.page'].search([ ('url', '=', '/home-support') ]) 
        else: 
            homepage = request.env['website.page'].search([ ('id', '=', '4') ]) 



        #if homepage and (homepage.sudo().is_visible or request.env.user.has_group('base.group_user')) and homepage.url != '/':
        if homepage and (homepage.sudo().is_visible or request.env.user.has_group('base.group_user')):
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