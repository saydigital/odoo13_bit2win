# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Consolidated Budget Management: Entry Model',
    'category': 'Accounting/Accounting',
    'version':'13.0.0.8',
    'description': """
Use budgets to compare actual with expected revenues and costs
--------------------------------------------------------------
""",
    'depends': ['syd_consolidated_base', 'account', 'account_budget', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/consolidated_budget_views.xml'
    ]
}
