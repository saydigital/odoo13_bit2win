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
            
            if homepage and request.env.user.has_group('base.group_portal') and homepage != '/':
                return request.env['ir.http'].reroute(homepage)
        # End custom fix 
        
        return super(Website,self).index(**kw)
