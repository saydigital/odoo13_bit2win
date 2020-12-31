from odoo import http, tools, _
from odoo.addons.website_slides.controllers.main import WebsiteProfile
from odoo import http, tools, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_profile.controllers.main import WebsiteProfile
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import AccessError, UserError
from odoo.http import request
from odoo.osv import expression

class WebsiteSlides(WebsiteProfile):
    
    @http.route('/slides/embed/<int:slide_id>', type='http', auth='public', website=True, sitemap=False)
    def slides_embed(self, slide_id, page="1", **kw):
        # Note : don't use the 'model' in the route (use 'slide_id'), otherwise if public cannot access the embedded
        # slide, the error will be the website.403 page instead of the one of the website_slides.embed_slide.
        # Do not forget the rendering here will be displayed in the embedded iframe

        # determine if it is embedded from external web page
        referrer_url = request.httprequest.headers.get('Referer', '')
        
        #PATCH FOR SLIDES
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url.slides.module')
        
        is_embedded = referrer_url and not bool(base_url in referrer_url) or False
        # try accessing slide, and display to corresponding template
        try:
            slide = request.env['slide.slide'].browse(slide_id)
            if is_embedded:
                request.env['slide.embed'].sudo()._add_embed_url(slide.id, referrer_url)
            values = self._get_slide_detail(slide)
            values['page'] = page
            values['is_embedded'] = is_embedded
            self._set_viewed_slide(slide)
            return request.render('website_slides.embed_slide', values)
        except AccessError: # TODO : please, make it clean one day, or find another secure way to detect
                            # if the slide can be embedded, and properly display the error message.
            return request.render('website_slides.embed_slide_forbidden', {})


