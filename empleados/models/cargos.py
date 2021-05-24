from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class cargos(models.Model):
    _name = 'empleados.cargos'

    _sql_constraints = [
        ('charge_record_constrain', 'UNIQUE(name)', 'Este cargo ya está registrado')
    ]

    @api.multi
    def unlink(self):
        # data = self[0]
        for rec in self:
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
        super(cargos, self).write({'state': 'draft'})
        # self.state = 'draft'

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

    @api.onchange('subtype')
    # @api.depends('is_medic')
    @api.multi
    def _set_medic(self):
        if self.subtype == 'medico':
            self.is_medic = True
            self.speciality = True
        elif self.subtype == 'administrativo':
            self.is_medic = False
            self.speciality = True
        else:
            self.is_medic = False
            self.speciality = False

    name = fields.Char(string="Cargos",
                       readonly=False, required=True)
    subtype = fields.Selection([('medico', 'Medico'),
                                ('servicio', 'Servicio'),
                                ('administrativo', 'Administrativo')], string="Tipo de cargo")
    is_medic = fields.Boolean(string="Es medico", readonly=True)
    speciality = fields.Boolean(string="Especialidad Requerida", readonly=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
