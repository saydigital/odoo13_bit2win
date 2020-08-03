# -*- coding: utf-8 -*-


{
    'name': "Helpdesk Environment SLA",
    'version': '0.0.1',
    'license': 'Other proprietary',
    'summary': """Helpdesk Environment SLA
    """,
    'author': "SayDigital",
    'website': "http://www.saydigital.it",
    'category' : 'Website',
    'depends': [
                'helpdesk',
                'website_helpdesk',
                'sale'
                ],
    'data':[
        'security/ir.model.access.csv',
        'views/views.xml'
    ],
    'installable' : True,
    'application' : False,
}

