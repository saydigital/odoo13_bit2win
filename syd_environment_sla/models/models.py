# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Environment(models.Model):
    _name = "helpdesk.environment"
    _description = "Environment"
    _order = "sequence"
    
    name = fields.Char('Name')
    helpdesk_ticket_ids = fields.One2many('helpdesk.ticket','environment_id',string="Tickets")
    sequence = fields.Integer('Sequence')
                
class HelpdeskSla(models.Model):
    _inherit = "helpdesk.sla"     
            
    environment_id = fields.Many2one("helpdesk.environment",string="Environment")
        
class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"            
       
    
    environment_id = fields.Many2one("helpdesk.environment",string="Environment")
    
    @api.model
    def _sla_reset_trigger(self):
        """ Get the list of field for which we have to reset the SLAs (regenerate) """
        res = super(HelpdeskTicket,self)._sla_reset_trigger()
        res + ['environment_id']
        return res
    
    def _sla_find(self):
        """ Find the SLA to apply on the current tickets
            :returns a map with the tickets linked to the SLA to apply on them
            :rtype : dict {<helpdesk.ticket>: <helpdesk.sla>}
        """
        tickets_map = {}
        sla_domain_map = {}

        def _generate_key(ticket):
            """ Return a tuple identifying the combinaison of field determining the SLA to apply on the ticket """
            fields_list = self._sla_reset_trigger()
            key = list()
            for field_name in fields_list:
                if ticket._fields[field_name].type == 'many2one':
                    key.append(ticket[field_name].id)
                else:
                    key.append(ticket[field_name])
            return tuple(key)

        for ticket in self:
            if ticket.team_id.use_sla:  # limit to the team using SLA
                key = _generate_key(ticket)
                # group the ticket per key
                tickets_map.setdefault(key, self.env['helpdesk.ticket'])
                tickets_map[key] |= ticket
                # group the SLA to apply, by key
                if key not in sla_domain_map:
                    sla_domain_map[key] = [('team_id', '=', ticket.team_id.id), ('priority', '<=', ticket.priority), ('stage_id.sequence', '>=', ticket.stage_id.sequence), '|', ('ticket_type_id', '=', ticket.ticket_type_id.id), ('ticket_type_id', '=', False),'|', ('environment_id', '=', ticket.environment_id.id), ('environment_id', '=', False)]

        result = {}
        for key, tickets in tickets_map.items():  # only one search per ticket group
            domain = sla_domain_map[key]
            result[tickets] = self.env['helpdesk.sla'].search(domain)  # SLA to apply on ticket subset

        return result
    