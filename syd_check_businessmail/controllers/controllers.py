# -*- coding: utf-8 -*-
# from odoo import http

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_module_resource

import inspect
import re
import os

#This email control class is also in the controller with some small difference. 
#TO-DO: Refactor code for a unique class
class WebsiteForm(WebsiteForm):
    #_inherit = ["syd_check_businessmail.business_mail_validator_mixin"]

    def extract_data(self, model, values):
        
        self._check_mails(values)
        
        return super(WebsiteForm, self).extract_data(model, values)
        
        
    def _check_mails(self, vals):
        #Have to activate the from the sales team page 
        #if(len(request.env['crm.team']) == 0):
        #    return True
           
        #if(request.env['crm.team'].search([('id','=', vals['team_id'])]).mail_control_active == False): 
        #    return True
        
        #if(request.env['crm.team'].search([('id','=', request.params['team_id'])]).mail_control_active)
        
        if ('email_from' in vals):
            if(vals['email_from'] != False):
                if(self._check_valid_mail(vals['email_from']) == False): 
                    raise ValidationError({"email_from": "Please, insert a valid corporate mail address"}) 

                if(self._is_business_mail(vals['email_from']) == False): 
                    request.env["syd_check_businessmail.refused_email"].sudo().create({"domain_failed": self._get_mail_address_domain(vals['email_from'])})
                    request._cr.commit()
                    raise ValidationError({"email_from": "Please, insert a valid corporate mail address"}) 
        
        if ('email_cc' in vals):
            if(vals['email_cc'] != False):
                if(self._check_valid_mail(vals['email_cc']) == False): 
                    raise ValidationError({"email_from": "Please, insert a valid corporate mail address in cc"}) 
        
                if(self._is_business_mail(vals['email_cc']) == False): 
                    request.env["syd_check_businessmail.refused_email"].sudo().create({"domain_failed": self._get_mail_address_domain(vals['email_cc'])})
                    request._cr.commit()
                    
                    raise ValidationError({"email_from": "Please, insert a valid corporate mail address in cc"}) 
        
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

