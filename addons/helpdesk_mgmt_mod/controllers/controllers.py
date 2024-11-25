# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskMgmtMod(http.Controller):
#     @http.route('/helpdesk_mgmt_mod/helpdesk_mgmt_mod', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_mgmt_mod/helpdesk_mgmt_mod/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_mgmt_mod.listing', {
#             'root': '/helpdesk_mgmt_mod/helpdesk_mgmt_mod',
#             'objects': http.request.env['helpdesk_mgmt_mod.helpdesk_mgmt_mod'].search([]),
#         })

#     @http.route('/helpdesk_mgmt_mod/helpdesk_mgmt_mod/objects/<model("helpdesk_mgmt_mod.helpdesk_mgmt_mod"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_mgmt_mod.object', {
#             'object': obj
#         })
