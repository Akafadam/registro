# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inventarios(models.Model):
    _name = 'inventarios.inventarios'

    _sql_constraints = [
        ('pacientes_record_birthyear', 'CHECK(date>current_date)', 'Esta fecha ya paso')
    ]

    product = fields.Many2one('productos.productos', string="Producto", required=True)
    reserve_type = fields.Selection(string="Tipo de Reserva", selection=[("egreso", "Egreso"), ("ingreso", "Ingreso")])
    cuantity = fields.Integer(string="Cantidad", required=True)
    date = fields.Date(string="Fecha", required=True)

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100