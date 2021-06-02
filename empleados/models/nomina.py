from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
class nomina(models.Model):
    _name = 'empleados.nomina'

    # @api.multi
    # def write(self, vals):
    #     return super(nomina, self).write(vals)

    @api.model
    def fill_rows(self):
        for rec in self.env['empleados.empleados'].search([('state','=','accepted')]):
            worked_hours = 0
            pay = 0
            for item in rec.attendance:
                worked_hours += item.worked_hours
                pay += item.pay
            vals2 = {
                'employee':rec.name,
                'id_card' : rec.id_card,
                'worked_hours' : worked_hours,
                'pay' : pay
            }
            # vals2['employee'] = rec.name
            row = self.env['empleados.nomina'].search([('id_card','=',rec.id_card)])
            if row:
                super(nomina, row).write(vals2)
            else:
                super(nomina, self).create(vals2)

    employee = fields.Char(string="Empleados")
    id_card = fields.Integer(string="Cedula")
    worked_hours = fields.Integer(string="Horas Trabajadas")
    pay = fields.Integer(string="Remuneracion")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
