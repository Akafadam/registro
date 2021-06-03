# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class productos(http.Controller):
    @http.route('/inventarios/inventarios/', type="json", auth='public', method=['POST'], csrf=False)
    def index(self, **post):
        print("\033[91m" + f"{post}")
        # for i in post: 
        #     print("\033[91m" + f"{i}")
        # print(type(post))
        # code = json.loads(post)
        # print(code)
        # print(post)
        # code = post.get('code')
        # print(code)
        print(request.env['inventarios.productos'].search([("code",'=', post["code"])]).name)
        return request.env['inventarios.productos'].search([("code",'=', post["code"])]).name

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