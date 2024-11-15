# -*- coding: utf-8 -*-

from odoo import models, fields, api


class maintenance_product_list(models.Model):
    _name = 'maintenance.product.list'
    _description = 'Lista de productos de mantenimiento'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    quantity = fields.Integer(required=True, string= 'Cantidad')
    request_id = fields.Many2one( "maintenance.request", string="Pedido Mantenimiento", required=True )
    equipment_id = fields.Many2one( "maintenance.equipment", string="Equipos de Mantenimiento", required=True )
    uom_id = fields.Many2one(related='product_id.uom_id', string='Unidad de medida')
    
