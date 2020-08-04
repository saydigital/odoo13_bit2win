# -*- coding: utf-8 -*-
{
    'name': "anonymous_ticket_comment",

    'description': """
       Replacing the member of the helpdesk team who wrote a comment with a configurable default user. 
    """,

    'author': "Saydigital",

    'category': 'Helpdesk',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk','base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/assets.xml', 
        'views/helpdesk_views.xml'
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ]
}
