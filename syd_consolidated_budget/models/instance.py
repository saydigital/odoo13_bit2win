# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
import xmlrpc.client

class Instance(models.Model):
    _inherit = "consolidated.instance"
    
    
    
    def get_and_update_models(self):
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            container_models = models.execute_kw(self.database, self.uid, self.password,
               'consolidated.budget.lines.container_model', 'search_read',
                [[['share', '=', True]]],
                {'fields': ['name', 'id'], 'limit': 1000})
            for c in container_models:
                m = self.env['consolidated.budget.lines.container_model'].search([('external_id','=',c['id'])],limit=1)
                if not m:
                    m = self.env['consolidated.budget.lines.container_model'].create({
                                                                                  'external_id':c['id'],
                                                                                  'name':c['name']
                                                                                  })
                else:
                    m.write({
                             'name':c['name']
                             })
                self._get_and_update_containers(m)
            return True
    
    def _get_and_update_containers(self,model_id):
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            containers = models.execute_kw(self.database, self.uid, self.password,
                'consolidated.budget.lines.container', 'search_read',
                [[['parent_id', '=', False],['model_id', '=', model_id.external_id]]],
                {'fields': ['name', 'id','sequence','sum'], 'limit': 1000})
            for c in containers:
                m = self.env['consolidated.budget.lines.container'].search([('external_id','=',c['id'])],limit=1)
                if not m:
                    
                    self.env['consolidated.budget.lines.container'].create({
                                                                                  'external_id':c['id'],
                                                                                  'name':c['name'],
                                                                                  'model_id':model_id.id,
                                                                                  'sequence':c['sequence'],
                                                                                  'sum':c['sum']
                                                                                  })
                else:
                    m.write({
                             'name':c['name'],
                             'parent_id':False,
                             'model_id':model_id.id,
                             'sequence':c['sequence'],
                             'sum':c['sum']
                             })
            containers = models.execute_kw(self.database, self.uid, self.password,
                'consolidated.budget.lines.container', 'search_read',
                [[['parent_id', '!=', False],['model_id', '=', model_id.external_id]]],
                {'fields': ['name', 'id','parent_id','sequence','sum'], 'limit': 1000})
            for c in containers:
                m = self.env['consolidated.budget.lines.container'].search([('external_id','=',c['id'])],limit=1)
                parent_id = self.env['consolidated.budget.lines.container'].search([('external_id','=',c['parent_id'][0])],limit=1)
                if not m:
                    
                    self.env['consolidated.budget.lines.container'].create({
                                                                                  'external_id':c['id'],
                                                                                  'name':c['name'],
                                                                                  'parent_id':parent_id.id,
                                                                                  'sequence':c['sequence'],
                                                                                  'model_id':model_id.id,
                                                                                  'sum':c['sum']
                                                                                  })
                else:
                    m.write({
                             'name':c['name'],
                            'parent_id':parent_id.id,
                            'sequence':c['sequence'],
                            'model_id':model_id.id,
                            'sum':c['sum']
                             })
            
            return True
    
    def _send_budget(self,budget_id):
        def _recursive_create_or_update(budget_id,company_id):
            id = self._create_or_update_budget(budget_id,company_id)
            
            for b in budget_id.consolidated_budget_line.filtered(lambda self:not self.parent_id):
                self._create_or_update_budget_line(b,id)
            for b in budget_id.consolidated_budget_line.filtered(lambda self:self.parent_id):
                self._create_or_update_budget_line(b,id)
                
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        company_id = self._get_external_company_id()
        if company_id:
            _recursive_create_or_update(budget_id,company_id)
            
        else:
            raise ValidationError('Company does not exists in the instance')
    
    def _create_or_update_budget(self,budget_id,company_id):
        ids = self._get_budget(budget_id,company_id)
        if ids:
            id = ids[0]
            self._update_budget(budget_id,id)
            return id
        else:
            return self._create_budget(budget_id,company_id)
        
    def _create_or_update_budget_line(self,budget_line_id,budget_id):
        external_parent_id = False
        if budget_line_id.parent_id:
            external_parent_id = self._get_budget_line(budget_line_id.parent_id,budget_id)
            if external_parent_id :
                external_parent_id = external_parent_id[0]
        ids = self._get_budget_line(budget_line_id,budget_id)
        if ids:
            id = ids[0]
            self._update_budget_line(budget_line_id,id)
            return id
        else:
            return self._create_budget_line(budget_id,budget_line_id,external_parent_id)
        
    def _get_budget(self,budget_id,company_id):
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids = models.execute_kw(self.database, self.uid, self.password,
            'consolidated.budget', 'search',
            [[
              ['company_id', '=', company_id],
              ['name', '=', budget_id.name],
              ['date_from', '=', budget_id.date_from],
              ['date_to', '=', budget_id.date_to],
              ]])
            return ids
    
    def _get_budget_line(self,budget_line_id,budget_id):
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            ids = models.execute_kw(self.database, self.uid, self.password,
            'consolidated.budget.lines', 'search',
            [[
              ['consolidated_budget_id', '=', budget_id],
              ['consolidated_budget_lines_container_id', '=', budget_line_id.consolidated_budget_lines_container_id.external_id],
              ['date_from', '=', budget_line_id.date_from],
              ['date_to', '=', budget_line_id.date_to]
              ]])
            return ids
        
    def _create_budget(self,budget_id,company_id):
        self.ensure_one()
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        id = models.execute_kw(self.database, self.uid, self.password, 'consolidated.budget','create', [{
            'company_id': company_id,
            'name': budget_id.name,
            'date_from':budget_id.date_from,
            'date_to':budget_id.date_to,
            'planned_amount':budget_id.planned_amount,
            'practical_amount':budget_id.practical_amount,
            'model_id':budget_id.model_id.external_id,
            'state':'sent-plan' if self.env.context.get('planned') else 'sent'
        }])
        return id
                                
    def _create_budget_line(self,budget_id,budget_line_id,external_parent_id):
        self.ensure_one()
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        id = models.execute_kw(self.database, self.uid, self.password, 'consolidated.budget.lines','create', [{
            'sequence' : budget_line_id.sequence,
            'name' : budget_line_id.name,
            'consolidated_budget_id' : budget_id,
            'date_from' : budget_line_id.date_from,
            'date_to' : budget_line_id.date_to,
            'planned_amount' : budget_line_id.planned_amount,
            'practical_amount' :budget_line_id.practical_amount,
            'description':budget_line_id.description,
            'parent_id':external_parent_id,
            'display_type':'line_section' if not bool(external_parent_id) else False,
            'consolidated_budget_lines_container_id':budget_line_id.consolidated_budget_lines_container_id.external_id
        }])
        return id
       
    def _update_budget(self,budget_id,ext_budget_id):
        self.ensure_one()
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        id = models.execute_kw(self.database, self.uid, self.password, 'consolidated.budget','write', [[ext_budget_id], {     
            'practical_amount':budget_id.practical_amount
        }])
        return id
    
    def _update_budget_line(self,budget_line_id,ext_budget_line_id):
        self.ensure_one()
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

        id = models.execute_kw(self.database, self.uid, self.password, 'consolidated.budget.lines','write', [[ext_budget_line_id], {     
            'practical_amount':budget_line_id.practical_amount
        }])
        return id
    
    