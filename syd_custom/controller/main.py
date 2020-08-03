# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteForm(WebsiteForm):

    @http.route('''/helpdesk_extended/submit''', type='http', auth="user", website=True)
    def website_helpdesk_form(self, **kwargs):
        partner_id = request.env.user.partner_id
        
        contracts = partner_id._get_contract_list_tuple()
        
        security_level = request.env['helpdesk.ticket']._fields['security_level'].selection
        impact = request.env['helpdesk.ticket']._fields['impact'].selection
        priority = request.env['helpdesk.ticket']._fields['priority'].selection
        environment_ids = request.env['helpdesk.environment'].search([(1,'=',1)])
        environments = []
        for e in environment_ids:
            environments += [(e.id,e.name)]
        return request.render("syd_custom.ticket_submit", {
                                                                      'contracts': contracts,
                                                                      'system_integrator':partner_id.is_system_integrator,
                                                                      'security_level': security_level,
                                                                      'impact': impact,
                                                                      'priority': priority,
                                                                      'environment': environments
                                                                      })

    