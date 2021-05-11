# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class empleados(models.Model):
    _name = 'empleados.empleados'

    _sql_constraints = [
        ('employees_record_id_card', 'UNIQUE(id_card)',
         'Este usuario ya esta registrado'),
        ('employees_record_pastdate',
         'CHECK(birthyear<current_date)', 'Esta fecha aun no existe')
    ]

    @api.constrains('birthyear')
    def _check_underage(self):
        timediff = relativedelta(date.today(), self.birthyear)
        yeardiff = timediff.years
        if yeardiff < 18:
            raise ValueError('El usuario debe ser mayor de edad')

    name = fields.Char(string="Nombre", required=True)
    birthyear = fields.Date(string="Año de nacimiento", required=True)
    charge = fields.Selection([('medico', 'Medico'),
                              ('servicio', 'Servicio'),
                              ('administrativo', 'Administrativo')],
                              string="Cargo", required=True)
    phone = fields.Integer(string="Número telefónico", required=True)
    id_card = fields.Integer(string="Cédula", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    arrive_time = fields.Float(string="Hora de Llegada")
    leave_time = fields.Float(string="Hora de salida")
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
