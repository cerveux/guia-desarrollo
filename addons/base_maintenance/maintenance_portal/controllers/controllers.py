# -*- coding: utf-8 -*-
from odoo import _, http
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request
from datetime import datetime
import werkzeug



# class MaintenanceController(http.Controller):
#      @http.route('/my/maintenance_req', type="http", auth='user', website=True)
#      def portal_my_requests(self, **kw):
#         maint_req = request.env["maintenance.request"].search([])
#         return request.render('maintenance_portal.portal_my_requests', { 'maint_req': maint_req })
    

class MaintenancePortalController(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        employee = request.env.user.employee_id
        request_count = request.env["maintenance.request"].search_count([("partner_id", "child_of", partner.id)])
        values["request_count"]=request_count
        return values
    
    @http.route(
      ['/my/maintenance_req', '/my/maintenance_req/page/<int:page>'],
      type="http",
      auth='user',
      website=True,
      )
    def portal_my_requests(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Mas Nuevo"), "order": "create_date desc"},
            "name": {"label": _("Nombre"), "order": "name"},
            "stage": {"label": _("Etapa"), "order": "stage_id"},
            "schedule": {
                "label": _("Fecha prevista"),
                "order": "schedule_date desc",
            },
            "close": {"label": _("Cierre"), "order": "close_date desc"},
            "priority": {"label": _("Prioridad"), "order": "maintenance_priority desc"},
        }
        searchbar_filters = {"all": {"label": _("All"), "domain": []}}
        for stage in request.env["maintenance.stage"].search([]):
            searchbar_filters.update(
                {
                    str(stage.id): {
                        "label": stage.name,
                        "domain": [("stage_id", "=", stage.id)],
                    }
                }
            )
        # default sort by order
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain += searchbar_filters[filterby]["domain"]

        pager = portal_pager(
            url="/my/maintenance_req",
            url_args={},
            total=values["request_count"],
            page=page,
            step=self._items_per_page,
        )
        maint_req = request.env["maintenance.request"].search(
          domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        values.update(
            {
                "date": date_begin,
                "maint_req": maint_req,
                "page_name": "maintenance",
                "pager": pager,
                "default_url": "/my/maintenance_req",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "searchbar_filters": searchbar_filters,
                "filterby": filterby,
            }
        )
        return request.render('maintenance_portal.portal_my_requests', values)

    @http.route(["/my/maintenance_req/<int:maintenance_id>"], type="http", auth="user", website=True)
    def portal_my_request(self, maintenance_id=None, **kw):
        maintenance_req = request.env["maintenance.request"].browse([maintenance_id])
        prioridad = maintenance_req["maintenance_priority"]
        priority = dict(request.env["maintenance.request"]._fields["maintenance_priority"].selection).items()
        for prior in priority:
          if prior[0] == prioridad:
            prioridad = prior[1]
        maintenance_req_sudo = maintenance_req.sudo()
        values = self._maintenance_get_page_view_values(maintenance_req_sudo, **kw)
        values["prioridad"] = prioridad
        return request.render("maintenance_portal.portal_maintenance_request_page", values )

    def _maintenance_get_page_view_values(self, maintenance_req, **kwargs):
        closed_stages = request.env["maintenance.stage"].search(
            [("done", "=", True)]
        )
        values = {
            "page_name": "maintenance",
            "maintenance": maintenance_req,
            "closed_stages": closed_stages,
        }

        if kwargs.get("error"):
            values["error"] = kwargs["error"]
        if kwargs.get("warning"):
            values["warning"] = kwargs["warning"]
        if kwargs.get("success"):
            values["success"] = kwargs["success"]

        return values

    @http.route("/new/maintenance_req", type="http", auth="user", website=True)
    def create_new_maint_request(self, **kw):
        equipment = request.env["maintenance.equipment"].search([])
        priority = dict(request.env["maintenance.request"]._fields["maintenance_priority"].selection).items()
        return request.render(
          "maintenance_portal.portal_create_request",
          {"equipment": equipment, "priority_opt": priority},
        )
        
    @http.route("/submitted/request", type="http", auth="user", website=True, csrf=True)
    def submit_ticket(self, **kw):
        equipment = 0
        if kw.get("req_equipment"):
          equipment = int(kw.get("req_equipment"))
        else:
          equipment = None
        vals = {
          "partner_id": request.env.user.partner_id.id,
          "owner_user_id": request.env.uid,
          "equipment_id": equipment,
          "maintenance_priority": kw.get("prior"),
          "description": kw.get("req_description"),
          "name": kw.get("request_name"),
          "maintenance_team_id": request.env["maintenance.team"].search([])[0].id,
          "kanban_state": "normal",
        }
        new_request = request.env["maintenance.request"].sudo().create(vals)
        new_request.message_subscribe(partner_ids=request.env.user.partner_id.ids)
        return werkzeug.utils.redirect("/my/maintenance_req")

    @http.route("/maintenance_req/close", type="http", auth="user")
    def maintenance_req_close(self, **kw):
        values = {}
        for field_name, field_value in kw.items():
            if field_name.endswith("_id"):
                values[field_name] = int(field_value)
            else:
                values[field_name] = field_value
        ticket = (
            http.request.env["maintenance.request"]
            .sudo()
            .search([("id", "=", values["maintenance_id"])])
        )
        ticket.stage_id = values.get("stage_id")

        return werkzeug.utils.redirect("/my/maintenance_req/" + str(ticket.id))