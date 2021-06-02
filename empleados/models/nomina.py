from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
class nomina(models.Model):
    _name = 'empleados.nomina'

    def fill_rows(self):
        for rec in self.env['empleados.empleados'].search([('state','=','accepted')]):
            vals2 = {
                'employee':rec.name,
                'id_card' : rec.id_card,
                'worked_hours' : rec.attendance.worked_hours,
                'pay' : rec.attendance.pay
            }
            # vals2['employee'] = rec.name
            super(nomina, self).create(vals2)

    employee = fields.Char(string="Empleados")
    id_card = fields.Integer(string="Cedula")
    worked_hours = fields.Integer(string="Horas Trabajadas")
    pay = fields.Integer(string="Remuneracion")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
