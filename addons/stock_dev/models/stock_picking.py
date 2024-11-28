# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Picking(models.Model):

    _inherit = "stock.picking"
    
    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket relacionado')
    
    
    @api.onchange('helpdesk_ticket_id')
    def _onchange_maintenance_request_id(self):
        if self.helpdesk_ticket_id:
            # Clear existing moves
            self.move_ids_without_package = [(5, 0, 0)]

            product_moves = []
            for product in self.helpdesk_ticket_id.product_structure_ids:
                product_moves.append((0, 0, {
                    'product_id': product.product_id.id,
                    'product_uom_qty': product.quantity,
                    'name': product.product_id.name,
                    'product_uom': product.uom_id.id,
                    'location_id': self.location_id,
                    'location_dest_id': self.location_dest_id
                }))
            self.move_ids_without_package = product_moves
