# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    partner_id = fields.Many2one('res.partner', string='Usuario Portal Solicitante' )
    department_id = fields.Many2one('hr.department', readonly=True, string='Departamento')
    acting_user_ids = fields.Many2many( 'res.users', string='Ejecutantes', 
                                        domain=lambda self: [('id', 'in', self._get_maintenance_team_user_ids())])
    maintenance_priority = fields.Selection([
        ( 'maquina_parada', '1- Máquina parada / producción detenida'),
        ( 'maquina_funcionando', '2- Máquina funcionando / necesidad de reparación'),
        ( 'no_afecta', '3- No afecta a la producción'),
        ( 'otro', '4- Otro / detallar en notas'),
    ],
                                            string='Prioridad')
    # mala práctica debería terminar con _ids un mejor nombre seria product_list_ids
    maintenance_product_list = fields.One2many( 'maintenance.product.list', 'request_id', string='Productos para mantenimiento' )
    
    
    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        self.department_id = self.equipment_id.department_id

    @api.model
    def _get_maintenance_team_user_ids(self):
        maintenance_teams = self.env['maintenance.team'].search([])
        user_ids = maintenance_teams.mapped('member_ids').ids
        return user_ids