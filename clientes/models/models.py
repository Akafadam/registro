# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class clientes(models.Model):
    _name = 'clientes.clientes'

    _sql_constraints = [
        ('clients_record_id_card', 'UNIQUE(id_card)',
         'Este usuario ya esta registrado'),
        ('clients_record_birthday', 'CHECK(birthyear<current_date)',
         'Esta fecha aun no existe'),
    ]

    # _constraints = [
    #     ('check_underage', 'El usuario debe ser mayor de edad', ['birthyear'])
    # ]

    @api.constrains('birthyear')
    def _check_underage(self):
        timediff = relativedelta(date.today(), self.birthyear)
        yeardiff = timediff.years
        if yeardiff < 18:
            raise ValueError('El usuario debe ser mayor de edad')

    name = fields.Char(string="Nombre", required=True)
    id_card = fields.Integer(string="CI", required=True)
    birthyear = fields.Date(string="Año de nacimiento", required=True)
    phone = fields.Integer(string="Número telefónico", required=True)
    email = fields.Char(string="Correo eletrónico", required=True)
    address = fields.Char(string="Dirección", required=True)
    # today = fields.Date.today()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
