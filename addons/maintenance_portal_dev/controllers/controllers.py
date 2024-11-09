# -*- coding: utf-8 -*-
# from odoo import http


# class MaintenancePortalDev(http.Controller):
#     @http.route('/maintenance_portal_dev/maintenance_portal_dev', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/maintenance_portal_dev/maintenance_portal_dev/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('maintenance_portal_dev.listing', {
#             'root': '/maintenance_portal_dev/maintenance_portal_dev',
#             'objects': http.request.env['maintenance_portal_dev.maintenance_portal_dev'].search([]),
#         })

#     @http.route('/maintenance_portal_dev/maintenance_portal_dev/objects/<model("maintenance_portal_dev.maintenance_portal_dev"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('maintenance_portal_dev.object', {
#             'object': obj
#         })
