# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from pytz import timezone


class citas(models.Model):
    _name = 'citas.citas'

    _sql_constraints = [
        ('revision_record_id_card', 'UNIQUE(time, date_time)',
         'Esta hora ya esta registrada'),
    ]

    @api.onchange('medic_data')
    def _set_specs(self):
        self.speciality = self.medic_data.speciality

    @api.constrains('date_time', 'time')
    def _check_schedule(self):
        right_now = datetime.now()
        ccs = timezone('America/Caracas')
        local_rn = right_now.astimezone(ccs)

        if self.date_time < date.today():
            raise ValueError('Esta fecha ya paso')

        elif self.date_time == date.today():
            if self.time < local_rn.hour:
                raise ValueError('Esta hora ya paso')
        elif self.time < self.medic_data.arrive_time or self.time > self.medic_data.leave_time:
            raise ValueError('El médico no ocupa esa hora')

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
    speciality = fields.Char(string="Especialidad Medica",
                             required=True, compute="_set_specs")
    medic_data = fields.Many2one(
        'empleados.empleados', string="Medico", required=True)


#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
