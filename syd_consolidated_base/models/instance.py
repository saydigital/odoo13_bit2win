# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
import xmlrpc.client

class Instance(models.Model):
    _name = "consolidated.instance"
    _description = "Consolidated Instance"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    name = fields.Char('Name', required=True)
    
    type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External'),
        ], 'Type', default='internal',required=True)
    company_hash = fields.Char('Company Hash') 
    company_id = fields.Many2one('res.company','Company',required=True)
    url = fields.Char('Url')
    username = fields.Char('Username')
    password = fields.Char('Password')
    database = fields.Char('Database')
    uid = fields.Integer('UID')
    external_version = fields.Char('External Version')
    
#### External     
    
    def test_connection(self):
        self.ensure_one()
        self._authenticate()
        self._version()    
        
    
    def _authenticate(self):
        self.ensure_one()
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        uid = common.authenticate(self.database, self.username, self.password, {})
        self.uid = uid
        return uid
    
    
    def _version(self):
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        res = common.version()
        self.external_version = res['server_version']
        
    def _get_external_company_id(self):
        self.ensure_one()
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        
        ids = models.execute_kw(self.database, self.uid, self.password,
            'res.company', 'search',
            [[['company_hash', '=', self.company_hash]]])
        if ids:
            return ids[0]
        else :
            return False
        
    
    
    def _get_partner(self,partner_id):
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids = models.execute_kw(self.database, self.uid, self.password,
            'res.partner', 'search',
            [[
              ['name', '=', partner_id.name],
              ]])
            return ids
    
    