# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import re
from odoo.exceptions import UserError, ValidationError


class empleados(models.Model):
    _name = 'empleados.empleados'

    # _sql_constraints = [
    #     ('employees_record_id_card', 'UNIQUE(id_card)',
    #      'Este usuario ya esta registrado'),
    #     ('employees_record_pastdate',
    #      'CHECK(birthyear<current_date)', 'Esta fecha aun no existe')
    # ]

    def validate(self):
        if self.name:
            pass
        else:
            raise UserError('Los datos de nombre estan vacios')
        if self.id_card:
            pass
        else:
            raise UserError('Los datos de la cedula estan vacios')
        if self.birthyear:
            pass
        else:
            raise UserError('Los datos de la fecha estan vacios')
        if self.charge:
            pass
        else:
            raise UserError('Los datos del cargo estan vacios')
        if self.email:
            pass
        else:
            raise UserError('Los datos del correo electronico estan vacios')
        if self.address:
            pass
        else:
            raise UserError('Los datos de la direccion estan vacios')
        if self.phone:
            pass
        else:
            raise UserError('Los datos del telefono estan vacios')
        if self.speciality:
            pass
        elif not self.is_medic:
            pass
        else:
            raise UserError('Los datos de la especialida estan vacios')
        if self.schedule:
            pass
        else:
            raise UserError('Los datos del horario estan vacios')
        self._check_id()
        self._check_date()
        self._check_underage()
        self._validate_email()
        self.validate_phone()
        self.state = 'accepted'

    def _check_date(self):
        if self.birthyear > date.today():
            raise UserError('Esta fecha aún no existe')

    @api.multi
    def unlink(self):
        # data = self[0]
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(empleados, self).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(empleados, self).write(vals)

    # @api.onchange('attendance')
    # @api.depends('attendance')
    # def _set_hours(self):
    #     print('\033[93m' + f'{self.attendance}')
    #     hours_list = []
    #     for item in self.attendance:
    #         hours_list.append(item.worked_hours)
    #     print('\033[93m' + f'{hours_list}')

    def invalidate(self):
        if self.attendance:
            raise UserError("El registro de empleado no puede ser invalidado porque hay asistencias con su nombre")
        if self.appointment_ids:
            raise UserError("El registro de empleado no puede ser invaidado por que hay una cita con su nombre")
        super(empleados, self).write({'state': 'draft'})
        # self.state = 'draft'

    @api.onchange('charge')
    @api.depends('charge')
    def _set_is_medic(self):
        for rec in self:
            if rec.charge.name == "Medico":
                rec.is_medic = True
            else:
                rec.is_medic = False

    # @api.constrains('birthyear')
    def _check_underage(self):
        if self.birthyear:
            timediff = relativedelta(date.today(), self.birthyear)
            yeardiff = timediff.years
            if yeardiff < 18:
                raise UserError('El usuario debe ser mayor de edad')

    def _check_id(self):
        for rec in self:
            if self.env['empleados.empleados'].search([('id_card','=', rec.id_card),('state','=','accepted')]):
                # print(self.env['citas.personas'].search([('id_card','=', self.id_card)]).name)
                raise UserError('Este usuario ya registrado')

    # @api.constrains('email')
    def _validate_email(self):
        if self.email:
            self.email.replace(" ", "")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                raise ValidationError("Invalido. Ingrese el Correo nuevamente")

    # @api.constrains('phone')
    def validate_phone(self):
        if self.phone:
            if self.phone:
                match = re.match('^[0]\d{10}$', self.phone)
            if not match:
                raise ValidationError('El Numero de Telefono no es Correcto')

    name = fields.Char(string="Nombre")
    birthyear = fields.Date(string="Año de nacimiento")
    charge = fields.Many2one('empleados.cargos', string="Cargo")
    phone = fields.Char(string="Número telefónico")
    id_card = fields.Integer(string="Cédula")
    email = fields.Char(string="Correo eletrónico")
    is_medic = fields.Boolean(compute="_set_is_medic",
                              default=False, store=True)
    address = fields.Char(string="Dirección")
    speciality = fields.Many2one(
        'empleados.especialidad', string="Especialidad/Grado")
    appointment_ids = fields.One2many(comodel_name='citas.citas', inverse_name='medic_id', domain=[('state','=','accepted')])
    schedule = fields.Many2one('empleados.horario', string="Horario")
    attendance = fields.One2many('empleados.asistencias', 'employee', domain=[('state','=','accepted')])
    # payroll = fields.Many2one('empleados.nomina', 'employee')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
    # state = fields.Selection([
    #     ('medic', 'Personal Medico'),
    #     ('service', 'Personal de Servicio'),
    #     ('admin', 'Personal Administrativo')
    # ])
