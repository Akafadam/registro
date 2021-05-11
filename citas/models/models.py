# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class citas(models.Model):
    _name = 'citas.citas'

    _sql_constraints = [
        ('revision_record_id_card', 'UNIQUE(time)', 'Esta hora ya esta registrada')]

    @api.constrains('time')
    def _check_schedule(self):
        if self.time >= 24 or self.time % 1 != 0:
            raise ValueError('Hora no permitida')

    date_time = fields.Date(string="Fecha", required=True)
    time = fields.Float(string="Hora", required=True)
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
