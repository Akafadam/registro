from odoo import models, fields, api

class dialogo(models.TransientModel):
    _name = 'citas.dialogo'

    password = fields.Char(string="Clave")