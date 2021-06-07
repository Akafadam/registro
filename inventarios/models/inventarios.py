# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import datetime


class inventarios(models.Model):
    _name = 'inventarios.inventarios'

    def validate(self):
        if self.product:
            pass
        else:
            raise UserError('El campo de productos está vacio')
        if self.reserve_type:
            pass
        else:
            raise UserError('El campo tipo de reserva está vacio')
        if self.cuantity:
            pass
        else:
            raise UserError('El campo de cantidad está vacio')
        if self.date:
            pass
        else:
            raise UserError('El campo de fecha está vacio')
        if self.date > datetime.date.today():
            raise UserError('La fecha no ha pasado')
        total = 0
        for rec in self.env['inventarios.inventarios'].search([('product', '=', self.product.id),
                                                               ('state', '=', 'accepted'),
                                                               ('date','<',self.date)]):
            if rec.reserve_type == 'ingreso':
                total += rec.cuantity
            if rec.reserve_type == 'egreso':
                total -= rec.cuantity
        if self.reserve_type == 'egreso':
            if total - self.cuantity < 0:
                raise UserError(
                    'El egreso excede la cantidad del producto')
        self.units = total
        self.state = 'accepted'

    def invalidate(self):
        total = 0
        for rec in self.env['inventarios.inventarios'].search([('product', '=', self.product.id),
                                                               ('state', '=', 'accepted'),
                                                               ('date','<',self.date)]):
            if rec.reserve_type == 'ingreso':
                total += rec.cuantity
            if rec.reserve_type == 'egreso':
                total -= rec.cuantity
        if self.reserve_type == 'ingreso':
            if total - self.cuantity < 0:
                raise UserError(
                    'El egreso excede la cantidad del producto')
        super(inventarios, self).write({'state': 'draft'})

    @api.depends('cuantity', 'reserve_type')
    @api.multi
    def _get_units(self):
        pass
        # total = 0
        # # data = self[0]
        # for rec in self.env['inventarios.inventarios'].search([('product', '=', self.product.id), ('state', '=', 'accepted')]):
        #     if rec.state == "accepted":
        #         if rec.reserve_type == 'ingreso':
        #             total += rec.cuantity
        #         if rec.reserve_type == 'egreso':
        #             total -= rec.cuantity

        #     rec.units = total

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(inventarios, self).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError(
                f"El registro fue validado, no puede ser editado´{self}")
        return super(inventarios, self).write(vals)

    product = fields.Many2one('inventarios.productos',
                              string="Producto")
    reserve_type = fields.Selection(string="Tipo de Reserva", selection=[
                                    ("egreso", "Egreso"), ("ingreso", "Ingreso")])
    cuantity = fields.Integer(string="Cantidad")
    date = fields.Date(string="Fecha")
    units = fields.Integer(string="Total")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
