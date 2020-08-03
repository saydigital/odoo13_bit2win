# -*- coding: utf-8 -*-


{
    'name': "Helpdesk Contract",
    'version': '0.0.1',
    'license': 'Other proprietary',
    'summary': """Helpdesk Extended
    """,
    'author': "SayDigital",
    'website': "http://www.saydigital.it",
    'category' : 'Website',
    'depends': [
                'helpdesk',
                'analytic',
                'website_helpdesk',
                'sale'
                ],
    'data':[
        'views/helpdesk_templates.xml',
        'views/views.xml'
    ],
    'installable' : True,
    'application' : False,
}

