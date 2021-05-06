# -*- coding: utf-8 -*-

from odoo import models, fields, api

class empleados(models.Model):
    _name = 'empleados.empleados'

    name = fields.Char(string="Nombre", required=True)
    birthyear = fields.Integer(string="Año de nacimiento", required=True)
    phone = fields.Integer(string="Número telefónico", required=True)
    id_card = fields.Integer(string="Cédula", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    arrive_time = fields.Selection([('9', '9:00'),
                                    ('10', '10:00'),
                                    ('11', '11:00'),
                                    ('12', '12:00'),
                                    ('13', '13:00'),
                                    ('14', '14:00'),
                                    ('15', '15:00'),
                                    ('16', '16:00'),
                                    ('17', '17:00')],
    string="Hora de Llegada")
    leave_time = fields.Selection([('9', '9:00'),
                                    ('10', '10:00'),
                                    ('11', '11:00'),
                                    ('12', '12:00'),
                                    ('13', '13:00'),
                                    ('14', '14:00'),
                                    ('15', '15:00'),
                                    ('16', '16:00'),
                                    ('17', '17:00')],
    string="Hora de salida")
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
