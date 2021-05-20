from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class cargos(models.Model):
    _name = 'cargos.cargos'

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

    def _set_medic(self):
        if self.is_medic:
            self.name = 'Medico'
            self.speciality = True

    name = fields.Char(string="Cargos", compute="_set_medic")
    speciality = fields.Boolean(string="Especialidad Requerida", compute="_set_medic")
    is_medic = fields.Boolean(string="¿Es medico?")