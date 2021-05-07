# -*- coding: utf-8 -*-

from odoo import models, fields, api

class empleados(models.Model):
    _name = 'empleados.empleados'

    _sql_constraints = [('employees_record','UNIQUE(id_card)', 'Este usuario ya esta registrado')]

    name = fields.Char(string="Nombre", required=True)
    birthyear = fields.Integer(string="Año de nacimiento", required=True)
    charge = fields.Selection([('medico', 'Medico'),
                              ('servicio', 'Servicio'),
                              ('administrativo', 'Administrativo')],
    string="Cargo")
    phone = fields.Integer(string="Número telefónico", required=True)
    id_card = fields.Integer(string="Cédula", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    arrive_time = fields.Selection([('09:00', '09:00'),
                                    ('10:00', '10:00'),
                                    ('11:00', '11:00'),
                                    ('12:00', '12:00'),
                                    ('13:00', '13:00'),
                                    ('14:00', '14:00'),
                                    ('15:00', '15:00'),
                                    ('16:00', '16:00'),
                                    ('17:00', '17:00')],
    string="Hora de Llegada")
    leave_time = fields.Selection( [('09:00', '09:00'),
                                    ('10:00', '10:00'),
                                    ('11:00', '11:00'),
                                    ('12:00', '12:00'),
                                    ('13:00', '13:00'),
                                    ('14:00', '14:00'),
                                    ('15:00', '15:00'),
                                    ('16:00', '16:00'),
                                    ('17:00', '17:00')],
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
