# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta
from lxml import etree

from odoo import models, fields, api, _
from odoo.addons.web_grid.models.models import END_OF, STEP_BY, START_OF
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    def action_notify_timesheet(self):  
        employee_id = self.env.user.employee_id
        note = _('New Timesheet submitted by %s') % ( employee_id.name )  
        employee_id.activity_schedule(
                    'syd_timesheet_notify.mail_timesheet_submitted',
                    note=note,
                    user_id=employee_id.timesheet_manager_id.id)
        return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'Thank you!!!',
                        'img_url': '/web/image/%s/%s/image_1024' % (employee_id.timesheet_manager_id._name, employee_id.timesheet_manager_id.id),
                        'type': 'rainbow_man',
                    }
                }