# -*- coding: utf-8 -*-

from odoo import models, fields, api

class productos(models.Model):
    _name = 'productos.productos'

    name = fields.Char(string="Nombre", required=True)
    code = fields.Integer(string="Código", required=True)
    cost = fields.Integer(string="Costo", required=True)
    qr_code = fields.Binary(string="Código QR", required=True)

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100