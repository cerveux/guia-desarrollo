# -*- coding: utf-8 -*-
# from odoo import http
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal

import werkzeug


class MaintenancePortalDev(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        maintenance_count = request.env["maintenance.request"].search_count([])
        values["maintenance_count"] = maintenance_count
        return values
        

    @route("/nuevo/mantenimiento", type="http", auth="user", website=True)
    def create_maintenance_request(self, **kw):
        equipment = request.env["maintenance.equipment"].search([])
        priorities = request.env["maintenance.request"].fields_get(allfields=["maintenance_priority"])["maintenance_priority"]["selection"]
        return request.render(
            "maintenance_portal_dev.portal_create_request",
            {"equipment": equipment, 'priorities': priorities},
        )
        
    @route("/submitted/request", type="http", auth="user", website=True, csrf=True)
    def submit_ticket(self, **kw):
        vals = {
            # "company_id": http.request.env.user.company_id.id,
            "name": kw.get("name"),
            "description": kw.get("description"),
            "equipment_id": kw.get("equipment"),
            "maintenance_priority": kw.get("priority"),
            "partner_id": request.env.user.partner_id.id
        }
        maintenance_request = request.env["maintenance.request"].sudo().create(vals)
        maintenance_request.message_subscribe(partner_ids=request.env.user.partner_id.ids)

        return werkzeug.utils.redirect("/my/requests")