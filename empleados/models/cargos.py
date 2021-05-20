from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class cargos(models.Model):
    _name = 'cargos.cargos'

    @api.multi
    def unlink(self):
        if self.name == 'Medico' or self.name == 'Personal Administrativo' or self.name == 'Personal de Servicio':
            raise UserError('Este cargo no se puede borrar')
        return super(cargos, self).unlink()

    name = fields.Char(string="Cargos")
    speciality = fields.Boolean(string="Especialidad")
    schedule = fields.Boolean(string="Horario")
