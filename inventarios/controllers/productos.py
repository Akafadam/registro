# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class productos(http.Controller):
    @http.route('/inventarios/inventarios/', type="json", auth='public', method=['POST'], csrf=False)
    def index(self, **post):
        print("\033[91m" + f"{post}")
        item = request.env['inventarios.productos'].search([("code","=",post["code"])])
        obj = {
            "name" : item.name,
            "code" : item.code,
            "cost" : item.cost,
            "units" : item.units,
        }

        result = json.dumps(obj)
        print(result)
        return result

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