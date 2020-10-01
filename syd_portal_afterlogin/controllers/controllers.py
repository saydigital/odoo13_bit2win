# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome



class NewAuthSignupHome(AuthSignupHome):
    
    @http.route()
    def web_login(self, *args, **kw):
        ensure_db()
        response = super(NewAuthSignupHome, self).web_login(*args, **kw)
        
        if request.httprequest.method == 'GET' and request.session.uid and not request.params.get('redirect') and request.website.url_afterlogin:
            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.website.url_afterlogin)
        return response