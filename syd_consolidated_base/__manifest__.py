# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Consolidated Base: Entry Model',
    'category': 'Base',
    'version': '13.0.0.1',
    'description': """
    Base module for consolidated data
--------------------------------------------------------------
""",
    'depends': ['account_budget'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml'
    ]
}
