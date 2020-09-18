# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class TicketCounter(http.Controller):
 
    @http.route(['/getTicketCounter'],type='json', auth='user', methods=['POST'], website=True, csrf=False)
    def getTicketCounter(self, **kw):
        
        tickets =  {'open': request.env['helpdesk.ticket'].search_count([  ("stage_id.name", "=", "New")   ]), 
                   'work_in_progress': request.env['helpdesk.ticket'].search_count([  ("stage_id.name", "=", "Working")   ]), 
                   'closed': request.env['helpdesk.ticket'].search_count([  ("stage_id.name", "=", "Solved")   ]), 
                   'waiting_answer': request.env['helpdesk.ticket'].search_count([  ("stage_id.name", "=", "Waiting for customer")   ]), 
                   'all': request.env['helpdesk.ticket'].search_count([])}

        return tickets