# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import inspect
import re
import os

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.modules.module import get_module_resource

class CrmTeam(models.Model):
    _inherit = "crm.team"
    
    mail_control_active = fields.Boolean('Email control active')


class Lead(models.Model):
    _name = "crm.lead"
    _inherit = ["crm.lead"]

    @api.model
    def create(self, vals):
        
        #In theory we no longer need backend control for Leads. 
        #But I leave commented because..you never know :)
        #if(request.is_frontend == False):
        #    self._check_mails(vals)
        
        return super(Lead, self).create(vals)
    
    def _check_mails(self, vals):
        
        #if(len(self.env['crm.team']) == 0):
        #    return True
        
        #if(self.env['crm.team'].search([('id','=', vals['team_id'])]).mail_control_active == False): 
        #    return True
        
        if ('email_from' in vals):
            if(vals['email_from'] != False):
                if(self._check_valid_mail(vals['email_from']) == False): 
                    raise ValidationError("Please, insert a valid corporate mail address") 

                if(self._is_business_mail(vals['email_from']) == False): 
                    self.env["syd_check_businessmail.refused_email"].sudo().create({"domain_failed": self._get_mail_address_domain(vals['email_from'])})
                    self._cr.commit()

                    raise ValidationError("Please, insert a valid corporate mail address") 
        
        if ('email_cc' in vals):
            if(vals['email_cc'] != False):
                if(self._check_valid_mail(vals['email_cc']) == False): 
                    raise ValidationError("Please, insert a valid corporate mail address") 
        
                if(self._is_business_mail(vals['email_cc']) == False): 
                    self.env["syd_check_businessmail.refused_email"].sudo().create({"domain_failed": self._get_mail_address_domain(vals['email_cc'])})
                    self._cr.commit()
                    
                    raise ValidationError("Please, insert a valid corporate mail address") 
        
    def _is_business_mail(self, email_address):
  
        file_path = get_module_resource('syd_check_businessmail', 'static', 'text', 'blacklist_domains.txt')
        
        with open(file_path) as file:
            black_list_domains = [line.rstrip() for line in file]        
        
        if(self._get_mail_address_domain(email_address) in black_list_domains ):
            return False
        else: 
            return True
    
    def _check_valid_mail(self, email_address):
        if (re.match(r"[^@]+@[^@]+\.[^@]+", email_address)):
            return True
        else:
            return False
        
    def _get_mail_address_domain(self, email_address):
        return email_address.split('@')[1]
