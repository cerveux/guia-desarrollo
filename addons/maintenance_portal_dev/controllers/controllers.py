# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class MaintenancePortalDev(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        maintenance_count = request.env["maintenance.request"].search_count([])
        values["maintenance_count"] = maintenance_count
        return values
