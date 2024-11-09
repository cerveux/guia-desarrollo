# -*- coding: utf-8 -*-

from odoo import models, fields, api, Command

class Picking(models.Model):
  _inherit = "stock.picking"

  ticket_id = fields.Many2one(
    comodel_name="helpdesk.ticket",
    string="Ticket relacionado",
    store=True,
    copied=True,
    ondelete="restrict"
  )

  @api.onchange("ticket_id")
  def _ticket_id_on_change(self):
    if self.ticket_id.id:
      model_string = ''
      self.move_ids_without_package = [(5, 0, 0)]
      if self.ticket_id.maintenance_request_id.id:
        model_string = 'maintenance_structure_id'
      else:
        model_string = 'product_structure_id'
      for rec in self.ticket_id[model_string]:
        self.move_ids_without_package = [(0,0, {
          'product_id': rec.product_id.id,
          'product_uom_qty': rec.quantity,
          'product_uom': rec.unit_of_measurement,
          'name': "Product",
          'location_id': self.location_id,
          'location_dest_id': self.location_dest_id
        })]

