# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class maintenance_portal_dev(models.Model):
#     _name = 'maintenance_portal_dev.maintenance_portal_dev'
#     _description = 'maintenance_portal_dev.maintenance_portal_dev'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
