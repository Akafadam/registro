# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from pytz import timezone
from odoo.exceptions import UserError, ValidationError


class citas(models.Model):
    _name = 'citas.citas'

    _sql_constraints = [
        ('revision_record_id_card', 'UNIQUE(time, date_time)',
         'Esta hora ya esta registrada'),
    ]

    def validate(self):
        data = self[0]
        data.state = 'accepted'

    def unlink(self):
        data = self[0]
        if data.state == "accepted":
            raise UserError('El registro fue validado, no puede ser eliminado')
        return super(citas, data).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser ejecutado")
        return super(citas, self).write(vals)

    @api.onchange('is_client')
    def _auto_fill(self):
        data = self[0]
        if data.is_client:
            data.pacient_data = data.client_data

    @api.onchange('medic_data')
    @api.depends('medic_data')
    def _set_specs(self):
        data = self[0]
        data.speciality = data.medic_data.speciality

    @api.constrains('date_time', 'time')
    def _check_schedule(self):
        right_now = datetime.now()
        ccs = timezone('America/Caracas')
        local_rn = right_now.astimezone(ccs)
        plusTwoMonth = timedelta(days=60) + date.today()

        if self.date_time < date.today():
            raise ValidationError('Esta fecha ya paso')

        elif self.date_time == date.today():
            if self.time < local_rn.hour:
                raise ValidationError('Esta hora ya paso')
        elif self.time < self.medic_data.arrive_time or self.time > self.medic_data.leave_time:
            raise ValidationError('El médico no ocupa esa hora')
        elif self.date_time > plusTwoMonth:
            raise ValidationError(
                'No se puede agendar una fecha para mas de dos meses en adelante')

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
        'citas.personas', string="Datos del cliente", required=True)
    is_client = fields.Boolean(string="¿Es el cliente el paciente?")
    pacient_data = fields.Many2one('citas.personas', string="Datos del paciente", required=True,
                                   compute="_auto_fill", readonly=False, store=True)
    speciality = fields.Char(string="Especialidad Medica", compute="_set_specs", store=True)
    medic_data = fields.Many2one(
        'empleados.empleados', string="Medico", required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")

#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
