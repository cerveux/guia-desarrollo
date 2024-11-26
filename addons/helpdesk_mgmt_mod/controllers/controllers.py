from odoo import http
from odoo.http import request
import logging
from odoo.addons.helpdesk_mgmt.controllers.main import HelpdeskTicketController

_logger = logging.getLogger(__name__)

class CustomHelpdeskTicketController(HelpdeskTicketController):
    
    @http.route("/new/ticket", type="http", auth="user", website=True)
    def create_new_ticket(self, **kw):
        type = http.request.env["helpdesk.ticket.type"].search([])
        email = http.request.env.user.email
        name = http.request.env.user.name
        return http.request.render(
            "helpdesk_mgmt.portal_create_ticket",
            {"types": type, "email": email, "name": name},
        )
