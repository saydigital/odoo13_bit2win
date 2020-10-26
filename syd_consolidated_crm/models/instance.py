# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
import xmlrpc.client

class Instance(models.Model):
    _inherit = "consolidated.instance"
     
    def align_lead_instance(self,lead_id):
        external_company_id = self._get_external_company_id()
        if lead_id.external_id:
            ids = self._get_lead(lead_id,external_company_id)
            if ids:
                id = ids[0]
                self._update_lead(lead_id,id)
                return id
        return self._create_lead(lead_id,external_company_id)
        
    
        
    def _get_lead(self,lead_id,external_company_id):
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids = models.execute_kw(self.database, self.uid, self.password,
            'crm.lead', 'search',
            [[
              ['company_id', '=', external_company_id],
              ['id', '=', lead_id.external_id],
              ]])
            return ids
        
    def _get_lead_stage(self,lead_id):
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids = models.execute_kw(self.database, self.uid, self.password,
            'crm.stage', 'search',
            [[
              ['name', '=', lead_id.stage_id.consolidated_stage_name]
              ]])
            return ids
    
    def _prepare_lead_field(self,lead_id,external_company_id):
        vals = {
            'name' : lead_id.name,
            'planned_revenue': lead_id.planned_revenue,
            'probability': lead_id.probability,
            'date_deadline':lead_id.date_deadline,
            'partner_name':lead_id.partner_name,
            'contact_name':lead_id.contact_name,
            'mobile':lead_id.mobile,
            'description':lead_id.description,
            'function':lead_id.function,
            'referred':lead_id.referred,
            'user_name':lead_id.user_id.name
        }
        ids = self._get_lead_stage(lead_id)
        if ids:
            vals.update({ 
                         'stage_id':ids[0]
                         })
        if lead_id.partner_id:
            ids = self._get_partner(lead_id.partner_id)
            if ids:
                vals.update({ 
                             'partner_id':ids[0]
                             })
        return vals
        
        
    def _create_lead(self,lead_id,external_company_id):
        self.ensure_one()
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        
        vals = self._prepare_lead_field(lead_id,external_company_id)
        id = models.execute_kw(self.database, self.uid, self.password, 'crm.lead','create', [vals])
        lead_id.external_id = id
        return id
        
       
    def _update_lead(self,lead_id,external_lead_id):
        self.ensure_one()
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        vals = self._prepare_lead_field(lead_id,external_company_id)
        id = models.execute_kw(self.database, self.uid, self.password, 'crm.lead','write', [[external_lead_id], vals])
        return id
    
   
    