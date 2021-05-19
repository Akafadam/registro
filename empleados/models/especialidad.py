from odoo import models, fields, api


class especialidad(models.Model):
    _name = 'especialidad.especialidad'

    name = fields.Char(string="Especialidad")
