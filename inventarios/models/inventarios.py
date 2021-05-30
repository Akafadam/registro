# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class inventarios(models.Model):
    _name = 'inventarios.inventarios'

    _sql_constraints = [
        ('pacientes_record_birthyear', 'CHECK(date>current_date)', 'Esta fecha ya paso')
    ]

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
        total = 0
        for rec in self.env['inventarios.inventarios'].search([('product', '=', self.product.id), ('state', '=', 'accepted')]):
            if rec.reserve_type == 'ingreso':
                total += rec.cuantity
            if rec.reserve_type == 'egreso':
                total -= rec.cuantity
        if self.reserve_type == 'egreso':
            if total - self.cuantity < 0:
                raise UserError(
                    'El egreso excede la cantidad del producto')
        self.units = total
        # if rec.reserve_type == 'egreso':
        #     if rec.units - rec.cuantity < 0:
        #         raise UserError('El egreso es mayor a la cantidad')
        # if self.reserve_type == 'egreso':
        self.state = 'accepted'

    def invalidate(self):
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
