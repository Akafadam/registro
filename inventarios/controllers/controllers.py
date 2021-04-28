# -*- coding: utf-8 -*-
from odoo import http

# class Inventarios(http.Controller):
#     @http.route('/inventarios/inventarios/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventarios/inventarios/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventarios.listing', {
#             'root': '/inventarios/inventarios',
#             'objects': http.request.env['inventarios.inventarios'].search([]),
#         })

#     @http.route('/inventarios/inventarios/objects/<model("inventarios.inventarios"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventarios.object', {
#             'object': obj
#         })