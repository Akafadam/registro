from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class nomina(models.Model):
    _name = 'empleados.nomina'

    employee = fields.One2many(
        'empleados.empleados', 'payroll', string="Empleados")
    worked_hours = fields.Many2one(
        'empleados.asistencia', string="Horas trabajadas")
    pay = fields.Integer()
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
