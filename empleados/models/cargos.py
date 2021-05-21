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

    @api.onchange('type')
    # @api.depends('is_medic')
    @api.multi
    def _set_medic(self):
        if self.type == 'medico':
            self.is_medic = True
            self.speciality = True
        elif self.type == 'administrativo':
            self.is_medic = False
            self.speciality = True
        else:
            self.is_medic = False
            self.speciality = False

    name = fields.Char(string="Cargos",
                       readonly=False, required=True)
    type = fields.Selection([('medico', 'Medico'),
                             ('servicio', 'Servicio'),
                             ('administrativo', 'Administrativo')],string="Tipo de cargo")
    is_medic = fields.Boolean(string="Es medico")
    speciality = fields.Boolean(string="Especialidad Requerida")

