# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

# ejercicio 7
class HelpdeskType(models.Model):

    _inherit = "helpdesk.ticket.type"
    
    access = fields.Boolean(string='Permiso de acceso', default=True)