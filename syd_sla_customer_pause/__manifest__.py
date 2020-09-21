# -*- coding: utf-8 -*-
{
    'name': "syd_sla_customer_pause", 

    'description': """
      
    """,

    'author': "Saydigital",

    'category': 'Helpdesk',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['mail','base','helpdesk'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml', 
        'views/helpdesk_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}