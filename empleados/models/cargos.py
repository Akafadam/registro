from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class cargos(models.Model):
    _name = 'cargos.cargos'

    _sql_constraints = [
        ('charge_record_constrain', 'UNIQUE(name)', 'Este cargo ya está registrado')
    ]

    # @api.multi
    # def unlink(self):
    #     if self.name == 'Medico':
    #         raise UserError('Este cargo no se puede borrar')
    #     return super(cargos, self).unlink()

    # @api.multi
    # def write(self, value):
    #     if self.name == 'Medico':
    #         raise UserError('Este cargo no se puede editar')
    #     return super(cargos, self).write(value)

    @api.onchange('is_medic')
    # @api.depends('is_medic')
    @api.multi
    def _set_medic(self):
        if self.is_medic:
            self.speciality = True

    name = fields.Char(string="Cargos",
                       readonly=False, required=True)
    speciality = fields.Boolean(
        string="Especialidad Requerida")
    is_medic = fields.Boolean(string="¿Es medico?")
