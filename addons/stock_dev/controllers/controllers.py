# -*- coding: utf-8 -*-
# from odoo import http


# class StockDev(http.Controller):
#     @http.route('/stock_dev/stock_dev', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_dev/stock_dev/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_dev.listing', {
#             'root': '/stock_dev/stock_dev',
#             'objects': http.request.env['stock_dev.stock_dev'].search([]),
#         })

#     @http.route('/stock_dev/stock_dev/objects/<model("stock_dev.stock_dev"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_dev.object', {
#             'object': obj
#         })
