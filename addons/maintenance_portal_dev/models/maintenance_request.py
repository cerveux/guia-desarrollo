# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    partner_id = fields.Many2one('res.partner', string='Usuario Portal Solicitante' )
    department_id = fields.Many2one('hr.department', readonly=True, string='Departamento')
    
    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        self.department_id = self.equipment_id.department_id
