# -*- coding: utf-8 -*-
# from odoo import http


# class AnonymousTicketComment(http.Controller):
#     @http.route('/anonymous_ticket_comment/anonymous_ticket_comment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anonymous_ticket_comment/anonymous_ticket_comment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anonymous_ticket_comment.listing', {
#             'root': '/anonymous_ticket_comment/anonymous_ticket_comment',
#             'objects': http.request.env['anonymous_ticket_comment.anonymous_ticket_comment'].search([]),
#         })

#     @http.route('/anonymous_ticket_comment/anonymous_ticket_comment/objects/<model("anonymous_ticket_comment.anonymous_ticket_comment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anonymous_ticket_comment.object', {
#             'object': obj
#         })
