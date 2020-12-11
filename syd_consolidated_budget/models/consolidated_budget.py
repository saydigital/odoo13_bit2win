# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

class ConsolidatedBudgetLinesContainerModel(models.Model):
    _name = "consolidated.budget.lines.container_model"    
    _inherit = ['consolidated.align_mixin']
    _description = "Consolidated Budget Line Container Model"
    
    name = fields.Char('Container Model')      
    container_ids = fields.One2many('consolidated.budget.lines.container','model_id',string="Containers")
    share = fields.Boolean('Share')
    company_id = fields.Many2one('res.company', 'Company')

class ConsolidatedBudget(models.Model):
    _name = "consolidated.budget"
    _description = "Consolidated Budget"
    _inherit = ['mail.thread', 'mail.activity.mixin','consolidated.align_mixin']
    _order = 'id'

    
    model_id = fields.Many2one('consolidated.budget.lines.container_model','Model')
    name = fields.Char('Budget Name',default="Enter name or model",help="Enter name or select model",store=True,compute="_change_name",inverse="_manual_name")
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    date_from = fields.Date('Start Date', required=True )
    date_to = fields.Date('End Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancelled'),
        ('confirm', 'Confirmed'),
        ('sent-plan','Sent Planned'),
        ('sent', 'Sent')
        ], 'Status', default='draft', index=True, required=True, readonly=True, copy=False, tracking=True)
    consolidated_budget_line = fields.One2many('consolidated.budget.lines', 'consolidated_budget_id', 'Budget Lines',
        states={'done': [('readonly', True)]}, copy=True)
    company_id = fields.Many2one('res.company', 'Company', required=True,
        default=lambda self: self.env.company)
    planned_amount = fields.Monetary('Sum Planned Value',compute="_value")
    practical_amount = fields.Monetary('Sum Practical Value',compute="_value")
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    
    def _manual_name(self):
        self.name = self.name
        
    @api.depends('model_id','date_to')
    def _change_name(self):
        for a in self:
            if a.model_id:
                a.name ="%s-%s"%(a.model_id.name,a.date_to.strftime("%m-%y"))
            else:
                a.name = _('Enter name')
            
    def action_populate_from_container(self):
        containers = self.env['consolidated.budget.lines.container'].search([('model_id','=',self.model_id.id)])
        for c in containers:
            self.env['consolidated.budget.lines'].create({
                                                              'date_from':self.date_from,
                                                              'date_to':self.date_to,
                                                              'consolidated_budget_lines_container_id':c.id,
                                                              'consolidated_budget_id':self.id,
                                                              'display_type':'line_section' if not bool(c.parent_id) else False,
                                                              'sequence':c.sequence
                                                              })
        
    def _value(self):
        for a in self:
                a.planned_amount = sum(b.planned_amount for b in a.consolidated_budget_line.filtered(lambda self: self.consolidated_budget_lines_container_id and self.consolidated_budget_lines_container_id.sum))
                a.practical_amount = sum(b.practical_amount for b in a.consolidated_budget_line.filtered(lambda self: self.consolidated_budget_lines_container_id and self.consolidated_budget_lines_container_id.sum))
                    
    def action_calc(self):
        self.consolidated_budget_line._compute_practical_amount()
        
    def action_budget_confirm(self):
        self.action_calc()
        self.write({'state': 'confirm'})

    def action_budget_draft(self):
        self.write({'state': 'draft'})

    def action_budget_validate(self):
        if self.instance_id:
            self.instance_id._send_budget(self)
        self.write({'state': 'sent'})
        
    def action_budget_validate_plan(self):
        if self.instance_id:
            self.instance_id.with_context(planned=True)._send_budget(self)
        self.write({'state': 'sent-plan'})

    def action_budget_cancel(self):
        self.write({'state': 'cancel'})

    def action_budget_done(self):
        self.write({'state': 'done'})


class ConsolidatedBudgetRule(models.Model):
    _name = "consolidated.budget.rule"
    _description = "Consolidated Budget Rule"
    
    name = fields.Char('Rule')
    model_name= fields.Selection([('account.analytic.line','Analytic'),
                                  ('account.move.line','General'),
                                  ('sale.order.line','Order'),
                                  ('crm.lead','Opportunity/Lead')
                                  
                                  ],string="Type",default="account.move.line")
    expected=fields.Boolean('Expected')
    filter_domain = fields.Char('Filter On', help=" Filter on the object")
    group_ids = fields.Many2many('account.analytic.group',string="Groups")
    analytic_ids = fields.Many2many('account.analytic.account',string="Analytic Accounts")
    account_ids = fields.Many2many('account.account',string="Accounts")
    partner_ids = fields.Many2many('res.partner',string="Customer/Vendor")
    product_ids = fields.Many2many('product.product',string="Product")
    
    company_id = fields.Many2one('res.company', 'Company', required=True,
        default=lambda self: self.env.company)
       

    
     
class ConsolidatedBudgetLinesContainer(models.Model):
    _name = "consolidated.budget.lines.container"
    _description = "Consolidated Budget Line Container"
    _parent_name = "parent_id"
    _parent_store = True
    _inherit = ['consolidated.align_mixin']
    _order = 'sequence'
    
    sequence = fields.Integer('Sequence')
    name = fields.Char('Container')
    model_id = fields.Many2one("consolidated.budget.lines.container_model",string="Model")
    parent_id = fields.Many2one('consolidated.budget.lines.container','Parent')
    child_ids = fields.One2many('consolidated.budget.lines.container','parent_id','Child')
    parent_path = fields.Char(index=True)
    company_id = fields.Many2one('res.company', 'Company', required=True,
        default=lambda self: self.env.company)
    sum = fields.Boolean('Sum',default=False)
    consolidated_budget_rule_id = fields.Many2one('consolidated.budget.rule','Rule',company_dependent=True)
    
    
    @api.constrains('parent_id', 'child_ids')
    def _check_subcontainer_level(self):
        for container in self:
            if container.parent_id and container.child_ids:
                raise ValidationError(_('Container %s cannot have several levels.' % (container.name,)))
    
class ConsolidatedBudgetLines(models.Model):
    _name = "consolidated.budget.lines"
    _description = "Consolidated Budget Line"
    _order = 'sequence,date_from'
    _inherit = ['consolidated.align_mixin']
    
    instance_id = fields.Many2one('consolidated.instance',related="consolidated_budget_id.instance_id",store=True,string="Instance")
    budget_name = fields.Char('Budget name',store=True,related="consolidated_budget_id.name")
    sequence = fields.Integer('sequence')
    name = fields.Char(compute='_compute_line_name')
    consolidated_budget_id = fields.Many2one('consolidated.budget', 'Budget', ondelete='cascade', index=True, required=True)
    
    parent_id = fields.Many2one('consolidated.budget.lines',string="Section")
    description = fields.Char('Description')
    child_ids = fields.One2many('consolidated.budget.lines','parent_id',string="Childs")
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    planned_amount = fields.Monetary(
        'Planned Amount',
        help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.")
    adjustment = fields.Monetary(string="Adjustment",help="Amount to adjust on calculated value.")
    practical_amount = fields.Monetary(string='Practical Amount',help="Amount really earned/spent.")
    
    company_id = fields.Many2one(related='consolidated_budget_id.company_id', comodel_name='res.company',
        string='Company', store=True, readonly=True)
    consolidated_budget_state = fields.Selection(related='consolidated_budget_id.state', string='Budget State', store=True, readonly=True)
    consolidated_budget_rule_id = fields.Many2one('consolidated.budget.rule','Rule',related="consolidated_budget_lines_container_id.consolidated_budget_rule_id")
    consolidated_budget_lines_container_id = fields.Many2one('consolidated.budget.lines.container', 'Budget Line Container')
    display_type = fields.Selection([
        ('line_section', 'Section'),
    ], default=False, help="Technical field for UX purpose.")
    
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        fields_list = {'practical_amount', 'planned_amount'}

        # Not any of the fields_list support aggregate function like :sum
        def truncate_aggr(field):
            field_no_aggr = field.split(':', 1)[0]
            if field_no_aggr in fields_list:
                return field_no_aggr
            return field
        fields = {truncate_aggr(field) for field in fields}
        result = super(ConsolidatedBudgetLines, self).read_group(
            domain, fields, groupby, offset=offset,
            limit=limit, orderby=orderby, lazy=lazy) 
        for group_line in result:
                # initialise fields to compute to 0 if they are requested
                if 'practical_amount' in fields and 'consolidated_budget_lines_container_id' not in group_line:
                    group_line['practical_amount'] = False
                if 'planned_amount' in fields and 'consolidated_budget_lines_container_id' not in group_line:
                    group_line['planned_amount'] = False
        return result
    
    @api.constrains('sequence')
    def calc_parent_id(self):
        for a in self:
            for line in self.search([('consolidated_budget_id','=',a.consolidated_budget_id.id)]):
                if line.display_type != False:
                    line.parent_id = False
                else:
                    parent_line = self.search([('consolidated_budget_id','=',line.consolidated_budget_id.id),('sequence','<',line.sequence),('display_type','=','line_section')],limit=1,order="sequence desc" )
                    line.parent_id = parent_line.id
            
    @api.model           
    def create(self,values):
        res = super(ConsolidatedBudgetLines,self).create(values)
        res.calc_parent_id()
        return res
    
    
    

    @api.depends("consolidated_budget_id", "consolidated_budget_lines_container_id")
    def _compute_line_name(self):
        #just in case someone opens the budget line in form view
        for record in self:
            computed_name = ''
            if record.consolidated_budget_lines_container_id:
                computed_name = record.consolidated_budget_lines_container_id.name
            record.name = computed_name

    def _calc_domain(self):
        domain = []
        date_to = self.date_to
        date_from = self.date_from
        line = self
        if line.consolidated_budget_rule_id:
                
                domain = [('date', '>=', date_from),('date', '<=', date_to)] 
                if (line.consolidated_budget_rule_id.model_name == 'sale.order.line'):
                    domain = [('order_id.date_order', '>=', date_from),('order_id.date_order', '<=', date_to)] 
                domain += (safe_eval(line.consolidated_budget_rule_id.filter_domain,  {}) if line.consolidated_budget_rule_id.filter_domain else [])
               
                
                if (line.consolidated_budget_rule_id.model_name == 'account.analytic.line'):
                    
                    if line.consolidated_budget_rule_id.account_ids :
                        domain += [('general_account_id','in',line.consolidated_budget_rule_id.account_ids.ids)]
                    if line.consolidated_budget_rule_id.analytic_ids :
                        domain += [('account_id','in',line.consolidated_budget_rule_id.analytic_ids.ids)]
                    if line.consolidated_budget_rule_id.partner_ids :
                        domain += [('partner_id','in',line.consolidated_budget_rule_id.partner_ids.ids)]
                    if line.consolidated_budget_rule_id.product_ids :
                        domain += [('product_id','in',line.consolidated_budget_rule_id.product_ids.ids)]
                    if line.consolidated_budget_rule_id.group_ids :
                        if len(line.consolidated_budget_rule_id.group_ids)>1:
                            domain += [('group_id','in',line.consolidated_budget_rule_id.group_ids.ids)]
                        else:
                            domain += [('group_id','child_of',line.consolidated_budget_rule_id.group_ids.id)]
                elif (line.consolidated_budget_rule_id.model_name == 'account.move.line'):
                    if line.consolidated_budget_rule_id.partner_ids :
                        domain += [('partner_id','in',line.consolidated_budget_rule_id.partner_ids.ids)]
                    if line.consolidated_budget_rule_id.account_ids :
                        domain += [('account_id','in',line.consolidated_budget_rule_id.account_ids.ids)]
                    if line.consolidated_budget_rule_id.analytic_ids :
                        domain += [('analytic_account_id','in',line.consolidated_budget_rule_id.analytic_ids.ids)]
                    if line.consolidated_budget_rule_id.product_ids :
                        domain += [('product_id','in',line.consolidated_budget_rule_id.product_ids.ids)]
                elif (line.consolidated_budget_rule_id.model_name == 'sale.order.line'):
                    if line.consolidated_budget_rule_id.partner_ids :
                        domain += [('order_id.partner_id','in',line.consolidated_budget_rule_id.partner_ids.ids)]
                    if line.consolidated_budget_rule_id.product_ids :
                        domain += [('product_id','in',line.consolidated_budget_rule_id.product_ids.ids)]
                    if line.consolidated_budget_rule_id.analytic_ids :
                        domain += [('order_id.analytic_account_id','in',line.consolidated_budget_rule_id.analytic_ids.ids)]    
                elif (line.consolidated_budget_rule_id.model_name == 'crm.lead'):
                    if line.consolidated_budget_rule_id.partner_ids :
                        domain += [('partner_id','in',line.consolidated_budget_rule_id.partner_ids.ids)]
                    
        return domain
    
    def _compute_practical_amount(self):
        for line in self:
            practical_amount = 0
            if line.consolidated_budget_rule_id :
                obj = self.env[line.consolidated_budget_rule_id.model_name]
                domain = line._calc_domain()
                where_query = obj._where_calc(domain)
                obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                if (line.consolidated_budget_rule_id.model_name == 'account.analytic.line'):
                    select = "SELECT SUM(amount) from " + from_clause + " where " + where_clause
                elif (line.consolidated_budget_rule_id.model_name == 'sale.order.line'):
                    select = "SELECT SUM(price_subtotal) from " + from_clause + " where " + where_clause
                elif (line.consolidated_budget_rule_id.model_name == 'crm.lead'):
                    if line.consolidated_budget_rule_id.expected:
                        select = "SELECT SUM(planned_revenue*(probability/100)) from " + from_clause + " where " + where_clause
                    else:
                        select = "SELECT SUM(planned_revenue) from " + from_clause + " where " + where_clause
                else:
                    select = "SELECT sum(credit)-sum(debit) from " + from_clause + " where " + where_clause
                self.env.cr.execute(select, where_clause_params)
                practical_amount = self.env.cr.fetchone()[0] or 0.0
                line.practical_amount = practical_amount + line.adjustment
            elif  line.consolidated_budget_lines_container_id and line.consolidated_budget_lines_container_id.sum and line.child_ids:
                line.practical_amount =  sum(l.practical_amount for l in line.child_ids)

    

    def action_open_budget_entries(self):
        action = {}
        domain = self._calc_domain()
        if self.consolidated_budget_rule_id and self.consolidated_budget_rule_id.model_name == 'account.analytic.line':
            # if there is an analytic account, then the analytic items are loaded
            action = self.env['ir.actions.act_window'].for_xml_id('analytic', 'account_analytic_line_action_entries')
        elif self.consolidated_budget_rule_id.model_name=='account.move.line':
            # otherwise the journal entries booked on the accounts of the budgetary postition are opened
            action = self.env['ir.actions.act_window'].for_xml_id('account', 'action_account_moves_all_a')
        elif self.consolidated_budget_rule_id.model_name=='sale.order.line':
            # otherwise the journal entries booked on the accounts of the budgetary postition are opened
            action = self.env['ir.actions.act_window'].for_xml_id('syd_consolidated_budget', 'action_sale_order_line')
        elif self.consolidated_budget_rule_id.model_name=='crm.lead':
            # otherwise the journal entries booked on the accounts of the budgetary postition are opened
            action = self.env['ir.actions.act_window'].for_xml_id('crm_enterprise', 'crm_lead_action_dashboard')        
        action['domain'] = domain
        return action

#     @api.constrains('date_from', 'date_to')
#     def _line_dates_between_budget_dates(self):
#         for line in self:
#             budget_date_from = line.consolidated_budget_id.date_from
#             budget_date_to = line.consolidated_budget_id.date_to
#             if line.date_from:
#                 date_from = line.date_from
#                 if date_from < budget_date_from or date_from > budget_date_to:
#                     raise ValidationError(_('"Start Date" of the budget line should be included in the Period of the budget'))
#             if line.date_to:
#                 date_to = line.date_to
#                 if date_to < budget_date_from or date_to > budget_date_to:
#                     raise ValidationError(_('"End Date" of the budget line should be included in the Period of the budget'))
