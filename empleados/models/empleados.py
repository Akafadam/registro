# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import re
from odoo.exceptions import UserError, ValidationError


class empleados(models.Model):
    _name = 'empleados.empleados'

    _sql_constraints = [
        ('employees_record_id_card', 'UNIQUE(id_card)',
         'Este usuario ya esta registrado'),
        ('employees_record_pastdate',
         'CHECK(birthyear<current_date)', 'Esta fecha aun no existe')
    ]

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
        else:
            raise UserError('Los datos de la especialida estan vacios')
        if self.schedule:
            pass
        else:
            raise UserError('Los datos del horario estan vacios')
        self.state = 'accepted'

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

    def invalidate(self):
        super(empleados, self).write({'state': 'draft'})
        # self.state = 'draft'

    @api.constrains('birthyear')
    def _check_underage(self):
        if self.birthyear:
            timediff = relativedelta(date.today(), self.birthyear)
            yeardiff = timediff.years
            if yeardiff < 18:
                raise ValueError('El usuario debe ser mayor de edad')

    @api.constrains('email')
    def _validate_email(self):
        if self.email:
            self.email.replace(" ", "")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                raise ValidationError("Invalido. Ingrese el Correo nuevamente")

    @api.constrains('phone')
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
    address = fields.Char(string="Dirección")
    speciality = fields.Many2one(
        'empleados.especialidad', string="Especialidad/Grado")
    schedule = fields.Many2one('empleados.horario', string="Horario")
    attendance = fields.One2many('empleados.asistencias', 'employee')
    payroll = fields.Many2one('empleados.nomina', 'employee')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
    # state = fields.Selection([
    #     ('medic', 'Personal Medico'),
    #     ('service', 'Personal de Servicio'),
    #     ('admin', 'Personal Administrativo')
    # ])
