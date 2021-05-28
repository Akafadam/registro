# -*- coding: utf-8 -*-

# from citas.models.citas import citas
from odoo import models, fields, api
from . import citas
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import re
from odoo.exceptions import UserError, ValidationError


class personas(models.Model):
    _name = 'citas.personas'

    _sql_constraints = [
        ('clients_record_id_card', 'UNIQUE(id_card)',
         'Este usuario ya esta registrado'),
        ('clients_record_birthday', 'CHECK(birthyear<current_date)',
         'Esta fecha aun no existe'),
    ]

    # _constraints = [
    #     ('check_underage', 'El usuario debe ser mayor de edad', ['birthyear'])
    # ]

    @api.multi
    def unlink(self):
        # data = self[0]
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(personas, self).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(personas, self).write(vals)

    def validate(self):
        if self.name:
            pass
        else:
            raise UserError('Los datos del nombre estan vacios')
        if self.birthyear:
            pass
        else:
            raise UserError('Los datos de la fecha de nacimiento estan vacios')
        if self.address:
            pass
        else:
            raise UserError('Los datos de la direccion estan vacios')
        if self.is_underage or self.id_card:
            pass
        else:
            raise UserError('Los datos de la cedula estan vacios')
        if self.is_underage or self.email:
            pass
        else:
            raise UserError('Los datos del correo estan vacios')
        if self.is_underage or self.phone:
            pass
        else:
            raise UserError('Los datos del telefono estan vacios')
        self.state = 'accepted'

    # @api.model
    # def create(self, vals):
    #     # print(citas)
    #     vals2 = vals
    #     vals2['state'] = 'accepted'
    #     return super(personas, citas).create(vals2)

    def invalidate(self):
        super(personas, self).write({'state': 'draft'})

    # @api.constrains('id_card')
    #     if self.id_type == 'j':

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

    @api.onchange('birthyear')
    def _check_underage(self):
        timediff = relativedelta(date.today(), self.birthyear)
        yeardiff = timediff.years
        if yeardiff < 18:
            self.is_underage = True
        else:
            self.is_underage = False

    name = fields.Char(string="Nombre")
    id_card = fields.Integer(string="CI")
    birthyear = fields.Date(string="Año de nacimiento")
    phone = fields.Char(string="Número telefónico")
    email = fields.Char(string="Correo eletrónico")
    id_type = fields.Selection([('v', 'V'), ('e', 'E'), ('j', 'J')])
    address = fields.Char(string="Dirección")
    is_underage = fields.Boolean()
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")

    # today = fields.Date.today()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
