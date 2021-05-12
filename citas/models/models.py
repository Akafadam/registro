# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class citas(models.Model):
    _name = 'citas.citas'

    _sql_constraints = [
        ('revision_record_id_card', 'UNIQUE(time, date_time)', 'Esta hora ya esta registrada'),
    ]

    @api.constrains('date_time', 'time')
    def _check_schedule(self):
        if self.date_time < date.today():
            raise ValueError('Esta fecha ya paso')
                
        else:
            right_now = datetime.now()
            if self.time < right_now.hour:
                raise ValueError('Esta hora ya paso')

    date_time = fields.Date(string="Fecha", required=True)
    time = fields.Selection([(7, '07:00'),
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
    string="Hora", required=True)
    client_data = fields.Many2one(
        'clientes.clientes', string="Datos del cliente", required=True)
    pacient_data = fields.Many2one(
        'pacientes.pacientes', string="Datos del paciente", required=True)
    speciality = fields.Selection([('geriatra', 'Geriatra'),
                                   ('pediatra', 'Pediatra'),
                                   ('cardiologo', 'Cardiologo'),
                                   ('hematologo', 'Hematologo'),
                                   ('neurologo', 'Neurologo'),
                                   ('nutriologo', 'Nutriologo'),
                                   ('traumatologo', 'Traumatologo')],
                                  string="Especialidad Medica", required=True)
    medic_data = fields.Many2one(
        'empleados.empleados', string="Medico", required=True)


#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
