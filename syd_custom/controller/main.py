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
        
        priority = []
        priorities = request.env['helpdesk.ticket']._fields['priority'].selection
        for pid, pname in priorities:
            if pid == '0':
                priority += [(pid,'Severity 1')]
            if pid == '1':
                priority += [(pid,'Severity 2')]
            if pid == '2':
                priority += [(pid,'Severity 3')]
            if pid == '3':
                priority += [(pid,'Severity 4')]
        environment_ids = request.env['helpdesk.environment'].search([(1,'=',1)])
        environments = []
        for e in environment_ids:
            environments += [(e.id,e.name)]
            
        type_ids = request.env['helpdesk.ticket.type'].search([(1,'=',1)])
        types = []
        for t in type_ids:
            types += [(t.id,t.name)]
        return request.render("syd_custom.ticket_submit", {
                                                                      'contracts': contracts,
                                                                      'system_integrator':partner_id.is_system_integrator,
                                                                      'types': types,
                                                                      'priority': priority,
                                                                      'environment': environments
                                                                      })

    