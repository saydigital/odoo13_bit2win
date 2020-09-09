# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteForm(WebsiteForm):

    @http.route('''/bit2win/form''', type='http', auth="user", website=True)
    def website_helpdesk_form(self, **kwargs):
        partner_id = request.env.user.partner_id
        
        contracts = partner_id._get_contract_list_tuple()
        
        priority = []
        priorities = request.env['helpdesk.ticket']._fields['priority'].selection
        for pid, pname in priorities:
            if pid == '0':
                priority += [(pid,'Cosmetic')]
            if pid == '1':
                priority += [(pid,'Major')]
            if pid == '2':
                priority += [(pid,'Minor')]
            if pid == '3':
                priority += [(pid,'Critical')]
        environment_ids = request.env['helpdesk.environment'].search([(1,'=',1)])
        environments = []
        for e in environment_ids:
            environments += [(e.id,e.name)]
        
        
        impact = []
        impact = request.env['helpdesk.ticket']._fields['impact'].selection 
        
        release_version_ids = request.env['helpdesk.release'].search([(1,'=',1)])
        releases = []

        for e in release_version_ids:
            releases += [(e.id,e.name)]
            
        reported_by_ids = request.env['helpdesk.reported'].search([(1,'=',1)])
        reported = []            
        
        for e in reported_by_ids:
            reported += [(e.id,e.name)]        
        
        type_ids = request.env['helpdesk.ticket.type'].search([(1,'=',1)])
        types = []
        for t in type_ids:
            types += [(t.id,t.name)]
            
        reason_why_id = request.env['helpdesk.ticket']._fields['reason_why_id']        
        
        return request.render("syd_custom.ticket_submit", {
                                                                      'contracts': contracts,
                                                                      'system_integrator':partner_id.is_system_integrator,
                                                                      'types': types,
                                                                      'priority': priority,
                                                                      'environment': environments,
                                                                      'impact':impact, 
                                                                      'release': releases, 
                                                                      'reported_by': reported, 
                                                                      'reason_why': reason_why_id
                                                                      })

    