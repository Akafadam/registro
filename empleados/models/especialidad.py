from odoo import models, fields, api


class especialidad(models.Model):
    _name = 'especialidad.especialidad'

    name = fields.Char(string="Especialidad")
    is_medic = fields.Boolean(string="¿Especialidad medica?")
