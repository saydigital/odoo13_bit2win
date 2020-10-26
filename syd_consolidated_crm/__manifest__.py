# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Consolidated CRM',
    'category': 'Sales',
    'description': """
CRM lead centralized
--------------------------------------------------------------
""",
    'depends': ['account','crm','syd_consolidated_base'],
    'data': [
        
        'views/crm.xml',
        'data/data.xml'
    ]
    
}
