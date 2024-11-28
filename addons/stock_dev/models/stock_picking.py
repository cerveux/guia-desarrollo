# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Picking(models.Model):

    _inherit = "stock.picking"
    
    help_desk_ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket relacionado')
