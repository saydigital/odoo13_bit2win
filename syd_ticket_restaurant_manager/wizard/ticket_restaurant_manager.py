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
import logging
from dateutil.parser import parse
from odoo.exceptions import UserError
import xlsxwriter

_logger = logging.getLogger(__name__)


class ticketRestaurantManager(models.TransientModel):
    _name = "wizard.ticket.restaurant"
    _description = "Add order lines to sales order"
    
    working_day = fields.Integer(string="Working day", required=True)
    start_date_search = fields.Datetime('Start date')
    end_date_search = fields.Datetime('End date')

    def export(self):
        filename = '{}{}{}'.format('export', datetime.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S'), '.xlsx')
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
    
    def _generate_ticket_report(self, worksheet=False, order_sudo=False):
        
        # date_search > date_start (contract)
        #            total_messages = self.env['mail.message'].search_count([('create_date', '>=',start), ('create_date', '<', end)])

        active_contracts = self._get_contracts_list()
        workdays_time = self.calculate_workdays()

        index = 0
        worksheet.set_column(0, 0, 30)

        for hr_contract in active_contracts:
            worksheet.set_row(index, 20)

            
            contract_calendar = hr_contract.resource_calendar_id
            employee_workdays_time = self.calculate_workdays(contract_calendar)
            
            
            
            worksheet.write(index, 0, hr_contract.employee_id.display_name)
            worksheet.write(index, 1, hr_contract.has_daily_ticket_restaurant)
            worksheet.write(index, 2, employee_workdays_time)

            index = index + 1
       
        return worksheet
    
    def _get_contracts_list(self):
        return self.env['hr.contract'].search([('date_start', '<=', self.start_date_search)]); 
    
    def calculate_workdays(self, contract_calendar):
        if(self.end_date_search):
            self.end_date_search = fields.Datetime.now()
        
        return contract_calendar.get_work_duration_data(self.start_date_search, self.end_date_search)
