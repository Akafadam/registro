from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
class nomina(models.Model):
    _name = 'empleados.nomina'

    def fill_rows(self):
        for rec in self.env['empleados.empleados'].search([('state','=','accepted')]):
            vals2 = {
                'employee':rec.name,
                'id_card' : rec.id_card 
            }
            # vals2['employee'] = rec.name
            super(nomina, self).create(vals2)

    employee = fields.Char(string="Empleados")
    id_card = fields.Integer()
    worked_hours = fields.Many2one(
        'empleados.asistencia', string="Horas trabajadas")
    pay = fields.Integer()
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
