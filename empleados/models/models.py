# -*- coding: utf-8 -*-

from odoo import models, fields, api

class empleados(models.Model):
    _name = 'empleados.empleados'

    name = fields.Char(string="Nombre", required=True)
    birthyear = fields.Integer(string="Año de nacimiento", required=True)
    phone = fields.Integer(string="Número telefónico", required=True)
    id_card = fields.Integer(string="Cédula", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    schedule = fields.Datetime(string="Horario")
    address = fields.Char(string="Dirección", required=True)
    speciality = fields.Selection([('geriatra', 'Geriatra'),
                                    ('pediatra', 'Pediatra'),
                                    ('cardiologo', 'Cardiologo'),
                                    ('hematologo', 'Hematologo'),
                                    ('neurologo', 'Neurologo'),
                                    ('nutriologo', 'Nutriologo'),
                                    ('traumatologo', 'Traumatologo')],
    string="Especialidad")
    worked = fields.Char(string="Horas trabajadas", required=True)
    pay = fields.Char(string="Remuneración", required=True)
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100