# -*- coding: utf-8 -*-


{
    'name': "Accrual Subscription",
    'version': '0.0.2',
    'license': 'Other proprietary',
    'summary': """Accrual Subscription
    """,
    'author': "Rapsodoo",
    'website': "http://www.rapsodoo.com",
    'category' : 'Account',
    'depends': [
                'account',
                'sale_subscription',
                'syd_accrual_helper'
                ],
    'data':[
       
        'views/views.xml'
        
    ],
    'installable' : True,
    'application' : False,
}

