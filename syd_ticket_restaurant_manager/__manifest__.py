# -*- coding: utf-8 -*-
{
    'name': "syd_ticket_restaurant_manager",

    'description': """
       Ticket restaurant manager ticket
    """,

    'author': "Rapsodoo",

    'version': '4.2',

    'depends': ['base', 'hr_contract', 'hr_payroll'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/ticket_restaurant_manager_wizard.xml'
    ]
}