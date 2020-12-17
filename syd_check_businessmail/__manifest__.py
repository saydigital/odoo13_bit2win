# -*- coding: utf-8 -*-
{
    'name': "syd_check_businessmail",

    'author': "Rapsodoo",

    'category': 'Uncategorized',
    'version': '2.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sales_team', 'crm'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ]
}
