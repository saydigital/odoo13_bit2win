# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteForm(WebsiteForm):

    @http.route('''/helpdesk_extended/submit''', type='http', auth="user", website=True)
    def website_helpdesk_form(self, **kwargs):
        partner_id = request.env.user.partner_id
        contracts = []
        if partner_id.is_system_integrator:
            for a in partner_id.helpdesk_analytic_account_ids:
                contracts.append([a.id,a.display_name])
        security_level = request.env['helpdesk.ticket']._fields['security_level'].selection
        impact = request.env['helpdesk.ticket']._fields['impact'].selection
        priority = request.env['helpdesk.ticket']._fields['priority'].selection
        environment = request.env['helpdesk.ticket']._fields['environment'].selection
        return request.render("syd_helpdesk_extended.ticket_submit", {
                                                                      'contracts': contracts,
                                                                      'system_integrator':partner_id.is_system_integrator,
                                                                      'security_level': security_level,
                                                                      'impact': impact,
                                                                      'priority': priority,
                                                                      'environment': environment
                                                                      })

    @http.route('/website_form/<string:model_name>', type='http', auth="user", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
       
        partner_id = request.env.user.partner_id 
        if partner_id.is_system_integrator:
            contract = request.env['account.analytic.account'].sudo().browse(int(kwargs.get('contract')))
            request.params['partner_id'] = contract.partner_id.id
        else:
            contract = partner_id._get_contract()
            request.params['partner_id'] = partner_id.id
        if contract:
            request.params['team_id'] = contract.helpdesk_team_id.id
            request.params['partner_created_id']=partner_id.id
                
        return super(WebsiteForm, self).website_form(model_name, **kwargs)