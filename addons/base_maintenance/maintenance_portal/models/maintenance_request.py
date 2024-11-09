# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    partner_id = fields.Many2one('res.partner', string="Usuario portal solicitante", store=True, copied=True, ondelete='set null')

    def get_maintenance_member_ids(self):
      self.env.cr.execute("SELECT * FROM maintenance_team_users_rel")
      values = self.env.cr.dictfetchall()
      result = [o['res_users_id'] for o in values]
      return [('id','in',result)]

    acting_user_ids = fields.Many2many(
      comodel_name='res.users',
      relation='maintenance_request_user_rel',
      column1='maintenance_request_id',
      column2='user_id',
      string='Ejecutantes',
      store=True,
      copied=True,
      ondelete='restrict',
      domain=get_maintenance_member_ids
    )

    user_id = fields.Many2one('res.users', string='Technician', tracking=True, domain=get_maintenance_member_ids)

    maintenance_priority = fields.Selection([
        ('1', '1- Maquina parada / producción detenida'),
        ('2', '2- Maquina funcionando / necesidad de reparación'),
        ('3', '3- No afecta a la producción'),
        ('4', '4- Otro / detallar en notas')
      ],
      store=True,
      copied=True,
      string="Prioridad")
    
    product_structure_ids=fields.One2many(
      string='Productos para mantenimiento',
      comodel_name='maintenance.product_list',
      inverse_name='maintenance_request_id',
      store=True,
      copied=True
    )

    equipment_structure_ids=fields.One2many(
      string='Productos para mantenimiento',
      related='equipment_id.product_structure_ids'
    )

    department_id = fields.Many2one('hr.department', related='equipment_id.department_id', string='Departamento', store=True, readonly=True)

    @api.onchange('equipment_id')
    def _get_department(self):
      if self.equipment_id:
        self.department_id = self.equipment_id.department_id

    def name_get(self):
      requests = []
      for rec in self:
        name = rec.code + ' - ' + rec.name
        requests.append((rec.id, name))
      return requests

    # def _get_maintenance_member_ids(self):
    #   member_list = []
    #   members = self.env['maintenance.maintenance_team'].search([])
    #   for rec in members:
    #     member_list.append(rec.member_ids)
    #   set_res = set(member_list)
    #   return list(set_res)