# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from pytz import timezone, utc
from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.equipment"

    # mala práctica debería terminar con _ids un mejor nombre seria product_list_ids
    maintenance_product_list = fields.One2many( 'maintenance.product.list', 'equipment_id', string='Productos para mantenimiento' )
    
    def _prepare_request_from_plan(self, maintenance_plan, next_maintenance_date):
        # Call the original method to get the default values
        values = super()._prepare_request_from_plan(maintenance_plan, next_maintenance_date)

        # Convert `next_maintenance_date` to UTC with Argentina timezone
        argentina_tz = timezone("America/Argentina/Buenos_Aires")
        local_date = fields.Date.from_string(next_maintenance_date)
        local_datetime = argentina_tz.localize(fields.Datetime.from_string(local_date), is_dst=None)
        utc_datetime = local_datetime.astimezone(utc)

        # Update the `schedule_date` to use the UTC format
        values["schedule_date"] = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

        return values
    
    
