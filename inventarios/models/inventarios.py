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

    @api.depends('cuantity', 'reserve_type')
    @api.multi
    def _get_units(self):
        total = 0
        for rec in self.env['inventarios.inventarios'].search([]):
            if rec.state == "accepted":
                if rec.reserve_type == 'ingreso':
                    total += rec.cuantity
                if rec.reserve_type == 'egreso':
                        total -= rec.cuantity
        print(total)
        if total < 0:
            raise UserError('El egreso no puede exceder la cantidad del producto')
        
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
        # default = 0
        # vals2 = vals
        # for rec in self:
        #     if rec.state == 'validated':
        #         if rec.reserve_type == 'ingreso':
        #             default += rec.cuantity
        #         if rec.reserve_type == 'egreso':
        #             default -= rec.cuantity
        # if default < 0:
        #     raise UserError('El egreso excede la cantidad de unidades')
        # else:
        #    vals2['units'] = default
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(inventarios, self).write(vals)

    # @api.model
    # def create(self, vals):
    #     default = 0
    #     vals2 = vals
    #     for rec in self:
    #         if rec.state == 'validated':
    #             if rec.reserve_type == 'ingreso':
    #                 default += rec.cuantity
    #             if rec.reserve_type == 'egreso':
    #                 default -= rec.cuantity
    #     if default < 0:
    #         raise UserError('El egreso excede la cantidad de unidades')
    #     else:
    #         vals2['units'] = default
    #     return super(inventarios, self).write(vals2)

    product = fields.Many2one('inventarios.productos',
                              string="Producto")
    reserve_type = fields.Selection(string="Tipo de Reserva", selection=[
                                    ("egreso", "Egreso"), ("ingreso", "Ingreso")])
    cuantity = fields.Integer(string="Cantidad")
    date = fields.Date(string="Fecha")
    units = fields.Integer(string="Unidades", compute="_get_units")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
