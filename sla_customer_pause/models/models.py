# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sla_customer_pause(models.Model):
#     _name = 'sla_customer_pause.sla_customer_pause'
#     _description = 'sla_customer_pause.sla_customer_pause'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
