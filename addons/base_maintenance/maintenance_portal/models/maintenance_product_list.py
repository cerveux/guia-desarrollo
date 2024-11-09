# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.http import request

class MaintenanceProductList(models.Model):
    _name = "maintenance.product_list"
    _description = "Listado de productos"

    quantity = fields.Float(string="Cantidad de producto", store=True, copied=True)
    product_id = fields.Many2one(
        string='Producto', 
        comodel_name='product.product', 
        ondelete='set null',
        store=True,
        copied=True
    )

    unit_of_measurement = fields.Many2one('uom.uom', related='product_id.uom_id', string='Unidad de medida', readonly=True, store=True, copied=True)

    maintenance_request_id = fields.Many2one('maintenance.request', string="Peticion de mantenimiento")

    maintenance_equipment_id = fields.Many2one('maintenance.equipment', string="Equipamiento")

    @api.onchange('product_id')
    def _compute_uom(self):
      for rec in self:
        rec.unit_of_measurement = rec.product_id.uom_id

