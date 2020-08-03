# -*- coding: utf-8 -*-
# from odoo import http


# class SlaCustomerPause(http.Controller):
#     @http.route('/sla_customer_pause/sla_customer_pause/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sla_customer_pause/sla_customer_pause/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sla_customer_pause.listing', {
#             'root': '/sla_customer_pause/sla_customer_pause',
#             'objects': http.request.env['sla_customer_pause.sla_customer_pause'].search([]),
#         })

#     @http.route('/sla_customer_pause/sla_customer_pause/objects/<model("sla_customer_pause.sla_customer_pause"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sla_customer_pause.object', {
#             'object': obj
#         })
