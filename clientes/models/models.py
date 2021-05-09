# -*- coding: utf-8 -*-

from odoo import models, fields, api


class clientes(models.Model):
    _name = 'clientes.clientes'

    _sql_constraints = [('clients_record', 'UNIQUE(id_card)',
                         'Este usuario ya esta registrado')]

    name = fields.Char(string="Nombre", required=True)
    id_card = fields.Integer(string="CI", required=True)
    birthyear = fields.Date(string="Año de nacimiento", required=True)
    phone = fields.Integer(string="Número telefónico", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    address = fields.Char(string="Dirección", required=True)
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
