
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class especialidad(models.Model):
    _name = 'empleados.especialidad'

    @api.multi
    def unlink(self):
        # data = self[0]
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(especialidad, self).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(especialidad, self).write(vals)

    def validate(self):
        self.state = 'accepted'

    def invalidate(self):
        if self.employees:
            raise UserError("No se puede invalidar la especilidad ya que hay un empleado con ella")
        super(especialidad, self).write({'state': 'draft'})
        # self.state = 'draft'

    _sql_constraints = [
        ('speciality_record_constrain', 'UNIQUE(name)',
         'Esta especialidad ya está registrada')
    ]

    name = fields.Char(string="Especialidad")
    employees = fields.One2many('empleados.empleados', 'speciality', domain=[('state','=','accepted')])

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
