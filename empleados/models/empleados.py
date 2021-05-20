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
    charge = fields.Many2one('cargos.cargos', string="Cargo", required=True)
    phone = fields.Integer(string="Número telefónico", required=True)
    id_card = fields.Integer(string="Cédula", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    arrive_time = fields.Selection([(7, '07:00'),
                                    (8, '08:00'),
                                    (9, '09:00'),
                                    (10, '10:00'),
                                    (11, '11:00'),
                                    (12, '12:00'),
                                    (13, '13:00'),
                                    (14, '14:00'),
                                    (15, '15:00'),
                                    (16, '16:00'),
                                    (17, '17:00'),
                                    (18, '18:00'),
                                    (19, '19:00'),
                                    (20, '20:00'),
                                    (21, '21:00'),
                                    (22, '22:00')],
                                   string="Hora de Llegada")
    leave_time = fields.Selection([(7, '07:00'),
                                   (8, '08:00'),
                                   (9, '09:00'),
                                   (10, '10:00'),
                                   (11, '11:00'),
                                   (12, '12:00'),
                                   (13, '13:00'),
                                   (14, '14:00'),
                                   (15, '15:00'),
                                   (16, '16:00'),
                                   (17, '17:00'),
                                   (18, '18:00'),
                                   (19, '19:00'),
                                   (20, '20:00'),
                                   (21, '21:00'),
                                   (22, '22:00')],
                                  string="Hora de salida")
    address = fields.Char(string="Dirección", required=True)
    speciality = fields.Many2one(
        'especialidad.especialidad', string="Especialidad")
    worked = fields.Char(string="Horas trabajadas")
    pay = fields.Char(string="Remuneración")
    state = fields.Selection([
        ('medic', 'Personal Medico'),
        ('service', 'Personal de Servicio'),
        ('admin', 'Personal Administrativo')
    ])
