from odoo import models, fields, api


class especialidad(models.Model):
    _name = 'especialidad.especialidad'

    _sql_constraints = [
        ('speciality_record_constrain', 'UNIQUE(name)',
         'Esta especialidad ya está registrada')
    ]

    name = fields.Char(string="Especialidad")
    is_medic = fields.Boolean(string="¿Especialidad medica?")
