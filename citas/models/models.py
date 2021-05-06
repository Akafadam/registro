# -*- coding: utf-8 -*-

from odoo import models, fields, api
from time import strftime

class citas(models.Model):
    _name = 'citas.citas'

    def check_schedule(self):
        time = self.date_time[-5:]

    date_time = fields.Datetime(string="Fecha y Hora", required=True)
    client_data = fields.Many2one('clientes.clientes', string="Datos del cliente", required=True)
    pacient_data = fields.Many2one('pacientes.pacientes', string="Datos del paciente", required=True)
    speciality = fields.Selection([('geriatra', 'Geriatra'),
                                    ('pediatra', 'Pediatra'),
                                    ('cardiologo', 'Cardiologo'),
                                    ('hematologo', 'Hematologo'),
                                    ('neurologo', 'Neurologo'),
                                    ('nutriologo', 'Nutriologo'),
                                    ('traumatologo', 'Traumatologo')],
    string="Especialidad Medica", required=True)
    medic_data = fields.Many2one('empleados.empleados', string="Medico", required=True)

#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100