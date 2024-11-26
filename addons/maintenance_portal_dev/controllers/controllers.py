# -*- coding: utf-8 -*-
# from odoo import http
from odoo.http import request, route
from odoo.exceptions import AccessError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

import werkzeug


class MaintenancePortalDev(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        maintenance_count = request.env["maintenance.request"].search_count([("partner_id", "=", partner.id)])
        values["maintenance_count"] = maintenance_count
        return values

    def _maintenance_request_check_access(self, request_id):
        maintenance_request = request.env["maintenance.request"].browse([request_id])
        request_sudo = maintenance_request.sudo()
        try:
            maintenance_request.check_access_rights("read")
            maintenance_request.check_access_rule("read")
        except AccessError:
            raise
        return request_sudo

    def _maintenance_get_page_view_values(self, maintenancenance, **kwargs):
        stages = request.env["maintenance.stage"].search([])
        values = {
                "page_name": "peticion",
                "maintenance": maintenancenance,
                "stages": stages
            }
        if kwargs.get("error"):
            values["error"] = kwargs["error"]
        if kwargs.get("warning"):
            values["warning"] = kwargs["warning"]
        if kwargs.get("success"):
            values["success"] = kwargs["success"]
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
    def submit_request(self, **kw):
        vals = {
            # "company_id": http.request.env.user.company_id.id,
            "name": kw.get("name"),
            "description": kw.get("description"),
            "equipment_id": int(kw.get("equipment")) if kw.get("equipment") else None,
            "maintenance_priority": kw.get("priority"),
            "partner_id": request.env.user.partner_id.id
        }
        maintenance_request = request.env["maintenance.request"].sudo().create(vals)
        maintenance_request.message_subscribe(partner_ids=request.env.user.partner_id.ids)

        return werkzeug.utils.redirect("/my/requests")
    
    @route(["/my/requests"], type="http", auth="user", website=True, csrf=True )
    def portal_my_requests( self, sortby=None, filterby=None, **kw ):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        MaintenanceRequests = request.env['maintenance.request']
        domain = []
        
        searchbar_sortings = {
            "creador": {"label": ("Creador"), "order": "partner_id"},
            "code": {"label": ("Número"), "order": "code"},
            "prioridad": {"label": ("Prioridad"), "order": "maintenance_priority"},
            "name": {"label": ("Nombre"), "order": "name"},
            "Equipamiento": {"label": ("Equipamiento"), "order": "equipment_id"},
            "stage": {"label": ("Etapa"), "order": "stage_id"},
            "date": {"label": ("Más nuevo"), "order": "create_date desc"},
            "realizacion": {"label": ("Fecha prevista"), "order": "schedule_date desc"},
            "cierre": {
                "label": ("Fecha de cierre"),
                "order": "close_date desc",
            },
        }
        searchbar_filters = {"all": {"label": ("All"), "domain": [("partner_id", "=", partner.id)]}}
        for stage in request.env["maintenance.stage"].search([]):
            searchbar_filters.update(
                {
                    str(stage.id): {
                        "label": stage.name,
                        "domain": [("stage_id", "=", stage.id), ("partner_id", "=", partner.id)],
                    }
                }
            )

        # default sort by order
        if not sortby:
            sortby = "creador"
        order = searchbar_sortings[sortby]["order"]

        # default filter by value
        if not filterby:
            filterby = "all"
        domain += searchbar_filters[filterby]["domain"]

        requests = MaintenanceRequests.search(domain, order=order)

        values.update(
            {
                "maintenance_requests": requests,
                "page_name": "Peticiones",
                "default_url": "/my/requests",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "searchbar_filters": searchbar_filters,
                "filterby": filterby,
            }
        )
        return request.render("maintenance_portal_dev.portal_my_requests", values)

    @route(["/request/update_stage"], type="http", auth="user", website=True)
    def update_stage(self, maintenance_id=None, stage_id=None, **kw):
        if not maintenance_id or not stage_id:
            return request.redirect("/my")
        
        try:
            maintenance = request.env["maintenance.request"].sudo().browse(int(maintenance_id))
            stage = request.env["maintenance.stage"].sudo().browse(int(stage_id))
            
            if maintenance and stage:
                maintenance.write({"stage_id": stage.id})
        except Exception as e:
            return request.redirect("/my?error=stage_update_failed")
    
        return request.redirect(f"/my/request/{maintenance_id}")

    @route(["/my/request/<int:request_id>"], type="http", website=True)
    def portal_my_request(self, request_id=None, **kw):
        try:
            request_sudo = self._maintenance_request_check_access(request_id)
        except AccessError:
            return request.redirect("/my")
        values = self._maintenance_get_page_view_values(request_sudo, **kw)
        return request.render("maintenance_portal_dev.portal_maintenance_request_page", values)

