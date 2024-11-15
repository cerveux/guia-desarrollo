# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.equipment"

    # mala práctica debería terminar con _ids un mejor nombre seria product_list_ids
    maintenance_product_list = fields.One2many( 'maintenance.product.list', 'equipment_id', string='Productos para mantenimiento' )
