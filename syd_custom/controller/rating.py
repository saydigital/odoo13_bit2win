# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.rating.controllers.main import Rating
from odoo.tools.translate import _
from odoo.tools.misc import get_lang

class Rating(Rating):
    
    @http.route(['/rating/<string:token>/<int:rate>/submit_feedback'], type="http", auth="public", methods=['post'], website=True)
    def submit_rating(self, token, rate, **kwargs):
        rating = request.env['rating.rating'].sudo().search([('access_token', '=', token)])
        if not rating:
            return request.not_found()
        record_sudo = request.env[rating.res_model].sudo().browse(rating.res_id)
        record_sudo.rating_apply(rate, token=token, feedback=kwargs.get('feedback'))
        lang = rating.partner_id.lang or get_lang(request.env).code
        
        base_url = request.website.url_afterlogin
        
        if base_url == None or base_url == False:
            base_url = "/"
        
        return request.env['ir.ui.view'].with_context(lang=lang).render_template('rating.rating_external_page_view', {
            'web_base_url': base_url,
            'rating': rating,
        })