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
        self.state = 'accepted'

    def invalidate(self):
        super(inventarios, self).write({'state': 'draft'})
        # self.state = 'draft'

    @api.multi
    def unlink(self):
        # data = self[0]
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(inventarios, self).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(inventarios, self).write(vals)

    product = fields.Many2one('inventarios.productos',
                              string="Producto")
    reserve_type = fields.Selection(string="Tipo de Reserva", selection=[
                                    ("egreso", "Egreso"), ("ingreso", "Ingreso")])
    cuantity = fields.Integer(string="Cantidad")
    date = fields.Date(string="Fecha")

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
