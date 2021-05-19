from odoo import models, fields, api


class cargos(models.Model):
    _name = 'cargos.cargos'

    name = fields.Char(string="Cargos")
