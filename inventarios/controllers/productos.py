# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class productos(http.Controller):
    @http.route('/inventarios/inventarios/', type="json", auth='public', method=['POST'], csrf=False)
    def index(self, **post):
        print(post)

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