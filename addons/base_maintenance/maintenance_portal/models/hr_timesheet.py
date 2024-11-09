from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    # def get_user_domain(self):
    #   if self.maintenance_request_id.id:
    #     return [('id', 'in', self.maintenance_request_id.acting_user_ids.ids)]
    #   else:
    #     return [('id', 'in', [])]
    def get_user_domain(self):
      self.env.cr.execute("SELECT * FROM maintenance_team_users_rel")
      values = self.env.cr.dictfetchall()
      result = [o['res_users_id'] for o in values]
      return [('id','in',result)]

    acting_user_id = fields.Many2one('res.users', string='Usuario Informante', domain=get_user_domain)