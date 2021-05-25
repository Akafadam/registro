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

    def validate(self):
        self.state = 'accepted'

    def invalidate(self):
        super(empleados, self).write({'state': 'draft'})
        # self.state = 'draft'

    @api.constrains('birthyear')
    def _check_underage(self):
        timediff = relativedelta(date.today(), self.birthyear)
        yeardiff = timediff.years
        if yeardiff < 18:
            raise ValueError('El usuario debe ser mayor de edad')

    @api.constrains('email')
    def _validate_email(self):
        self.email.replace(" ", "")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValidationError("Invalido. Ingrese el Correo nuevamente")

    @api.constrains('phone')
    def validate_phone(self):
        if self.phone:
            match = re.match('^[0]\d{10}$', self.phone)
        if not match:
            raise ValidationError('El Numero de Telefono no es Correcto')

    name = fields.Char(string="Nombre", required=True)
    birthyear = fields.Date(string="Año de nacimiento", required=True)
    charge = fields.Many2one('empleados.cargos', string="Cargo", required=True)
    phone = fields.Char(string="Número telefónico", required=True)
    id_card = fields.Integer(string="Cédula", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    address = fields.Char(string="Dirección", required=True)
    speciality = fields.Many2one(
        'empleados.especialidad', string="Especialidad/Grado")
    worked = fields.Char(string="Horas trabajadas")
    pay = fields.Char(string="Remuneración")
    arrive_time = False
    leave_time = False
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
    # state = fields.Selection([
    #     ('medic', 'Personal Medico'),
    #     ('service', 'Personal de Servicio'),
    #     ('admin', 'Personal Administrativo')
    # ])
