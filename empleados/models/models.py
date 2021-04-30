# -*- coding: utf-8 -*-

from odoo import models, fields, api

class empleados(models.Model):
    _name = 'empleados.empleados'

    name = fields.Char(string="Nombre", required=True)
    date = fields.Datetime(string="Fecha", required=True)
    birthyear = fields.Integer(string="Año de nacimiento", required=True)
    phone = fields.Integer(string="Número telefónico", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    schedule = fields.Datetime(string="Horario", required=True)
    address = fields.Char(string="Dirección", required=True)
    speciality = fields.Char(string="Especialidad", required=True)
    worked = fields.Char(string="Horas trabajadas", required=True)
    pay = fields.Char(string="Remuneración", required=True)
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100