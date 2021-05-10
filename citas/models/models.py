# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class citas(models.Model):
    _name = 'citas.citas'

    # _sql_constraints = [
    #     ('revision_record_id_card', 'UNIQUE(date_time)',
    # 'Esta hora ya esta registrada')]

    @api.constrains('date_time')
    def _check_schedule(self):
        if self.date_time < datetime.now():
            raise ValueError('Esta fecha y hora ya pasaron')

        timediff = relativedelta(self.date_time, datetime.now())
        hourdiff = timediff.hours
        if hourdiff < 1:
            raise ValueError('Esta hora ya está reservada')

    date_time = fields.Datetime(string="Fecha y Hora", required=True)
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
