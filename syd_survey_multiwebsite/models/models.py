# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.http import request
import werkzeug.utils
from email.policy import default

class Survey(models.Model):
    _inherit = "survey.survey"
    
    public_url = fields.Char("Public link", compute="_compute_survey_url")
    website_id = fields.Many2one('website',string="Website")
    
    def _compute_survey_url(self):
        """ Computes a public URL for the survey """
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for survey in self:
            if survey.website_id:
                survey.public_url = urls.url_join(survey.website_id.domain, "survey/start/%s" % (survey.access_token))
            else:
                survey.public_url = urls.url_join(base_url, "survey/start/%s" % (survey.access_token))
            
