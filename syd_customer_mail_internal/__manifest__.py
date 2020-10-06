# -*- coding: utf-8 -*-
{
    'name': "Customer Mail Internal",

    'description': """
       Replacing the mail  message for customer to avoid bounce. 
    """,

    'author': "Rapsodoo",

    'category': 'Helpdesk',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['mail','base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
         'views/views.xml',
        
    ],

   
}
