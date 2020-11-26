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

    def export(self):
        filename = '{}{}{}'.format('export',datetime.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S'),'.xlsx')
        path = os.path.join(tempfile.gettempdir(), filename)
        
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet('Ticket Restaurant')
        worksheet = self._generate_ticket_report(worksheet)
        workbook.close()
        file = open(path,'rb')
        
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
        worksheet.set_column(0, 1, 30)
        
        worksheet.write(0, 0, 'Products')
       
        return worksheet