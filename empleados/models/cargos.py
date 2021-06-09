from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class cargos(models.Model):
    _name = 'empleados.cargos'

    _sql_constraints = [
        ('charge_record_constrain', 'UNIQUE(name)', 'Este cargo ya está registrado')
    ]

    @api.multi
    def unlink(self):

        for rec in self:
            if rec.name == 'Medico':
                raise UserError('Este registro no se puede borrar')
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(cargos, self).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(cargos, self).write(vals)

    def validate(self):
        self.state = 'accepted'

    def invalidate(self):
        if self.employees:
            raise UserError("No se puede invalidar el cargo por que hay un empleado que lo está usando")
        super(cargos, self).write({'state': 'draft'})

    name = fields.Char(string="Cargos",
                       readonly=False, required=True)
    employees = fields.One2many('empleados.empleados', 'charge', domain=[('state','=','accepted')])
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
