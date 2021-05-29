# -*- coding: utf-8 -*-
from . import personas
from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from pytz import timezone
from odoo.exceptions import UserError, ValidationError

hours = [
    (0, '00:00'),
    (1, '01:00'),
    (2, '02:00'),
    (3, '03:00'),
    (4, '04:00'),
    (5, '05:00'),
    (6, '06:00'),
    (7, '07:00'),
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
    (22, '22:00'),
    (23, '22:00')
]


class citas(models.Model):
    _name = 'citas.citas'

    _sql_constraints = [
        ('revision_record_id_card', 'UNIQUE(time, date_time)',
         'Esta hora ya esta registrada'),
    ]

    def validate(self):
        if self.date_time:
            pass
        else:
            raise UserError('Los datos de fecha estan vacios')
        if self.time:
            pass
        else:
            raise UserError('Los datos de hora estan vacios')
        if self.client_data:
            pass
        else:
            raise UserError('Los datos del cliente estan vacios')
        if self.pacient_data:
            pass
        else:
            raise UserError('Los datos del paciente estan vacios')
        if self.medic_data:
            pass
        else:
            raise UserError('Los datos del medico estan vacios')
        if self.speciality:
            pass
        else:
            raise UserError('Los datos de especialidad estan vacios')
        self.state = 'accepted'

    def invalidate(self):
        super(citas, self).write({'state': 'draft'})

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(citas, self).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(citas, self).write(vals)

    @api.onchange('is_client')
    def _auto_fill(self):
        if self.is_client:
            self.pacient_data = self.client_data

    @api.onchange('search_by', 'speciality')
    def set_domain_for_teacher(self):
        if self.search_by == 'especialidad':
            class_obj = self.env['empleados.empleados'].search(
                [('speciality', '=', self.speciality.id)])
            print(class_obj)
            speciality_list = []
            for data in class_obj:
                speciality_list.append(data.id)

            res = {}
            res['domain'] = {'medic_data': [
                ('id', 'in', speciality_list), ('state', '=', 'accepted')]}
            return res
        else:
            res = {}
            res['domain'] = {'medic_data': []}
            return res

    @api.constrains('date_time', 'time')
    def _check_schedule(self):
        right_now = datetime.now()
        ccs = timezone('America/Caracas')
        local_rn = right_now.astimezone(ccs)
        plusTwoMonth = timedelta(days=60) + date.today()

        if self.date_time:
            if self.date_time < date.today():
                raise ValidationError('Esta fecha ya paso')
            elif self.date_time == date.today():
                if self.time < local_rn.hour:
                    raise ValidationError('Esta hora ya paso')
        if self.time:
            if self.time < self.medic_data.schedule.arrive_time or self.time > self.medic_data.schedule.leave_time:
                raise ValidationError('El médico no ocupa esa hora')
        if self.date_time:
            if self.date_time > plusTwoMonth:
                raise ValidationError(
                    'No se puede agendar una fecha para mas de dos meses en adelante')

    date_time = fields.Date(string="Fecha")
    time = fields.Selection(hours, string="Hora")
    client_data = fields.Many2one(
        'citas.personas', string="Datos del cliente")
    is_client = fields.Boolean(string="Autocompletar paciente")
    pacient_data = fields.Many2one('citas.personas', string="Datos del paciente",
                                   compute="_auto_fill", readonly=False, store=True)
    speciality = fields.Many2one('empleados.especialidad', string="Especialidad Medica",
                                 related="medic_data.speciality", store=True)
    medic_data = fields.Many2one(
        'empleados.empleados', string="Medico")
    search_by = fields.Selection(
        [('medico', 'Medico'), ('especialidad', 'Especialidad')], default='medico')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
