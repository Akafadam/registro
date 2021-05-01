# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inventarios(models.Model):
    _name = 'inventarios.inventarios'

    product = fields.Char(string="Producto", required=True)
    reserve_type = fields.Selection(string="Tipo de Reserva", selection=[("egreso", "Egreso"), ("ingreso", "Ingreso")])
    cuantity = fields.Integer(string="Cantidad", required=True)
    date = fields.Datetime(string="Fecha", required=True)

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100