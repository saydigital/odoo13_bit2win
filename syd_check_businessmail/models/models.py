# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import inspect
import re
import os


class Lead(models.Model):
    _inherit = 'crm.lead'
    
    @api.model
    def create(self, vals):
        
        if(vals['email_from'] != False):
            if(self._check_valid_mail(vals['email_from']) == False): 
                raise ValidationError("Please, insert a valid email address")
    
            if(self._is_business_mail(vals['email_from']) == False): 
                raise ValidationError("Plese, insert a business mail") 
        
        if(vals['email_cc'] != False):
            if(self._check_valid_mail(vals['email_cc']) == False): 
                raise ValidationError("Please, insert a valid cc email address")   
    
            if(self._is_business_mail(vals['email_cc']) == False): 
                 raise ValidationError("Plese, insert a business mail in cc field")     
        
        return super(Lead, self).create(vals)

    def _is_business_mail(self, email_address):
  
        directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))        
        complete_file_path = os.path.join(directory_path, 'blacklist_domains.txt')
        
        with open(complete_file_path) as file:
            black_list_domains = [line.rstrip() for line in file]        
        
        if(email_address.split('@')[1] in black_list_domains ):
            return False
        else: 
            return True
    
    def _check_valid_mail(self, email_address):
        if (re.match(r"[^@]+@[^@]+\.[^@]+", email_address)):
            return True
        else:
            return False
