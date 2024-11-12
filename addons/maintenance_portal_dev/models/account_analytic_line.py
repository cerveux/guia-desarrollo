# © 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    
    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    user_id = fields.Many2one(
                                'res.users',
                                string='Usuario informante',
                                default=_default_user,
                                domain=lambda self: [('id', 'in', self._get_maintenance_team_user_ids())])
    
    @api.model
    def _get_maintenance_team_user_ids(self):
        maintenance_teams = self.env['maintenance.team'].search([])
        user_ids = maintenance_teams.mapped('member_ids').ids
        return user_ids
