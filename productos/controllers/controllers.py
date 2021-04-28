# -*- coding: utf-8 -*-
from odoo import http

# class Productos(http.Controller):
#     @http.route('/productos/productos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/productos/productos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('productos.listing', {
#             'root': '/productos/productos',
#             'objects': http.request.env['productos.productos'].search([]),
#         })

#     @http.route('/productos/productos/objects/<model("productos.productos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('productos.object', {
#             'object': obj
#         })