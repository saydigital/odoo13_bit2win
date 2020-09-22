# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class TicketCounter(http.Controller):
 
    @http.route(['/getTicketCounter'], type='json', auth='user', methods=['POST'], website=True, csrf=False)
    def getTicketCounter(self, **kw):
        
        tickets = {'open': request.env['helpdesk.ticket'].search_count([  ("stage_id.name_for_customer", "=", "Open")  ]),
                   'work_in_progress': request.env['helpdesk.ticket'].search_count([  ("stage_id.name_for_customer", "=", "Work in progress")   ]),
                   'closed': request.env['helpdesk.ticket'].search_count([  ("stage_id.name_for_customer", "=", "Closed")   ]),
                   'waiting_answer': request.env['helpdesk.ticket'].search_count([  ("stage_id.name_for_customer", "=", "Waiting for customer")   ]),
                   'rejected': request.env['helpdesk.ticket'].search_count([  ("stage_id.name_for_customer", "=", "Rejected")   ]),
                   'all': request.env['helpdesk.ticket'].search_count([])}

        return tickets
