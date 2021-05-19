from odoo import models, fields, api


class especialidad(models.Model):
    _name = 'especialidad.especialidad'

    speciality = fields.Char(string="Especialidad")
