# -*- coding: utf-8 -*-
{
    'name': "ticket_restaurant_manager",

    'description': """
        Module to manage Ticket Restaurant
    """,

    'author': "Rapsodoo",

    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
