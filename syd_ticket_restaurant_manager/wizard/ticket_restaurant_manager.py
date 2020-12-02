# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import csv
from csv import DictWriter
import base64
import xlrd
import tempfile
import binascii
import os
from io import StringIO, BytesIO
import time
import datetime
from datetime import datetime
import logging
from dateutil.parser import parse
from odoo.exceptions import UserError
import xlsxwriter
from datetime import timedelta
import math
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ticketRestaurantManager(models.TransientModel):
    _name = "wizard.ticket.restaurant"
    _description = "Add order lines to sales order"
    
    working_days = fields.Integer(string="Working days")
    start_date_search = fields.Date('Start date', required=True)
    end_date_search = fields.Date('End date', required=True)

    def export(self):
        filename = '{}{}{}'.format('ticket_rest_export_', datetime.now().strftime('_%Y-%m-%d_%H-%M'), '.xlsx')
        path = os.path.join(tempfile.gettempdir(), filename)
        
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet('Ticket Restaurant')
        
        # Here I build the sheet
        worksheet = self._generate_ticket_report(worksheet)
        
        workbook.close()
        file = open(path, 'rb')
        vals = {'name': filename,
                'type':'binary',
                'public':True,
                'datas':base64.b64encode(file.read())
                }
        
        attachment_id = self.env['ir.attachment'].create(vals)
        file.close()
        
        return{
            'type':'ir.actions.act_url',
            'url':'/web/content/{}?download=true'.format(attachment_id.id),
            'target':'self'
            }        
    
    #Se ho almeno un confirm, error  
    
    def _generate_ticket_report(self, worksheet=False, order_sudo=False):

        active_contracts = self._get_contracts_list()

        index = 3
        worksheet.set_column(0, 0, 30)
        worksheet.set_column(0, 1, 30)
        worksheet.set_column(0, 2, 30)
        
        worksheet.set_row(0, 20)
        worksheet.write(0, 0, "From: " + self.start_date_search.strftime("%d/%m/%Y"))
        worksheet.write(0, 1, "To: " + self.end_date_search.strftime("%d/%m/%Y"))
        
        worksheet.write(1, 0, "")
        
        worksheet.write(2, 0, "Employee")
        worksheet.write(2, 1, "Has Ticket?")
        worksheet.write(2, 2, "Quantity")

        for hr_contract in active_contracts:
            worksheet.set_row(index, 20)
            
            contract_calendar = hr_contract.resource_calendar_id
            employee_workdays_time = self._calculate_employee_workdays(contract_calendar, hr_contract.employee_id)

            worksheet.write(index, 0, hr_contract.employee_id.display_name)
            worksheet.write(index, 1, self._has_ticket_restaurant(hr_contract))
            
            if(self._has_ticket_restaurant(hr_contract) == "YES"):
                worksheet.write(index, 2, employee_workdays_time)

            index = index + 1
       
        return worksheet
    
    def _has_ticket_restaurant(self, hr_contract):
        if(hr_contract.has_daily_ticket_restaurant):
            return "YES"
        else:
            return "NO"
    
    def _get_contracts_list(self):
        return self.env['hr.contract'].search([('date_start', '<=', self.start_date_search)], order='employee_id asc') 
    
    def _calculate_employee_workdays(self, contract_calendar, employee_id):
        if(self.end_date_search == False):
            self.end_date_search = fields.Datetime.now()
            
        leaves_to_approve = self.env['hr.leave'].search_count([('state', '=', 'confirm'), ('employee_id', '=', employee_id.id), ('date_from', '>=', self.start_date_search), ('date_to', '<=', self.end_date_search)])

        if(leaves_to_approve > 0 ):
            raise ValidationError(_('Please, approve or refuse all the leaves requests'))
    
        #aggiungere valide al controllo     
        leaves_number = self.env['hr.leave'].search([('state', '=', 'validate'), ('employee_id', '=', employee_id.id), ('date_from', '>=', self.start_date_search), ('date_to', '<=', self.end_date_search)])
        total_leaves_employee = 0   
        
        if(leaves_number != False):
            for hr_leave in leaves_number:
                if(hr_leave.number_of_days > 0.5):
                    total_leaves_employee = total_leaves_employee + math.ceil(hr_leave.number_of_days)
        
        return self._calculate_workindays_time_range(contract_calendar) - int(total_leaves_employee)

    def _calculate_workindays_time_range(self, contract_calendar):
        if(self.working_days > 0):
            return self.working_days
        else:
            datetime_start = datetime.combine(self.start_date_search, datetime.min.time())
            datetime_end = datetime.combine(self.end_date_search, datetime.min.time())
            
            return math.floor(contract_calendar.get_work_duration_data(datetime_start, datetime_end + timedelta(days=1))['days'])
