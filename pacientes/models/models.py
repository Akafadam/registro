# -*- coding: utf-8 -*-

from odoo import models, fields, api


class pacientes(models.Model):
    _name = 'pacientes.pacientes'

    _sql_constraints = [
        ('pacients_record_id_card', 'UNIQUE(id_card)', 'Este usuario ya esta registrado'),
        ('pacientes_record_birthyear', 'CHECK(birthyear<current_date)', 'Esta fecha aun no existe')
    ]

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
