# -*- coding: utf-8 -*-
{
    'name': "Custom B2W",
    'version': '0.1.16',
    'license': 'Other proprietary',
    'summary': """Helpdesk Extended
    """,
    'author': "SayDigital",
    'website': "http://www.saydigital.it",
    'category' : 'Website',
    'depends': [
                'portal',
                'helpdesk',
                'analytic',
                'website_helpdesk',
                'sale',
                'syd_environment_sla',
                'syd_helpdesk_contract',
                'website', 
                'website_slides', 
                'rating'
                ],
    'data':[
        'data/data.xml',
        'views/helpdesk_templates.xml',
        'wizard/wizard.xml',
        'views/views.xml',
        'views/asset.xml',
        'views/snippet.xml',
        'views/rating_template.xml',
        'views/helpdesk_portal_templates.xml',
        'views/fix_css.xml',
        'security/ir.model.access.csv'
    ],
    'installable' : True,
    'application' : False,
}