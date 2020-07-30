from odoo import api, fields, models, _

class Message(models.Model):
    _inherit = 'mail.message'
 
    communication_user = fields.Many2one('res.user', 'User')