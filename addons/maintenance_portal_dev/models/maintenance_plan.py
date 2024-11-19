# Copyright 2019-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import models, api, fields
from odoo.exceptions import ValidationError


class MaintenancePlan(models.Model):
    _inherit = "maintenance.plan"
    
    product_structure_ids = fields.One2many( 'maintenance.product.list', 'plan_id', string='Productos para mantenimiento' )

    @api.model
    def create(self, vals):
        
        
        start_maintenance_date = vals.get('start_maintenance_date')
        weekday = fields.Date.from_string(start_maintenance_date).weekday()
        
        calendar_40_hours = self.env['resource.calendar'].browse(1)
        
        if not calendar_40_hours:
            raise ValueError("Hubo un problema y no se encontró el calendario.")
        
        is_working = any(att.dayofweek == str(weekday) for att in calendar_40_hours.attendance_ids)
        
        if not is_working:
            raise ValidationError("No se puede asignar un día no laboral.")
        

        return super().create(vals)