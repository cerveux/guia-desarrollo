# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HelpdeskTicket(models.Model):

    _inherit = "helpdesk.ticket"
    
    product_structure_ids = fields.One2many('maintenance.product.list', 'helpdesk_ticket_id', string='Listado de productos')
    maintenance_request_id = fields.Many2one('maintenance.request', string='Petición de mantenimiento')
