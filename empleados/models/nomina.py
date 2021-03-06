from odoo import models, fields, api
import calendar
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime

class nomina(models.Model):
    _name = 'empleados.nomina'

    # @api.multi
    # def write(self, vals):
    #     return super(nomina, self).write(vals)

    def _last_day(self, year, month):
        last_day = calendar.monthrange(year, month)[1]
        # print('\033[94m' + f"{last_day}")
        return date(year, month, last_day)

    @api.model
    def fill_rows(self):
        current_year = date.today().year
        current_month = date.today().month
        start = None
        end = None

        if date.today().day <= 15:
            start = self._last_day(current_year, current_month - 1)
            end = date(current_year, current_month, 15)
        else:
            start = date(current_year, current_month, 16)
            end = self._last_day(current_year, current_month)

        for rec in self.env['empleados.empleados'].search([('state','=','accepted')]):
            worked_hours = 0
            pay = 0

            for item in rec.attendance:
                if item.date >= start and item.date <= end:
                    worked_hours += item.worked_hours
                    pay += item.pay

            vals2 = {
                'employee':rec.name,
                'id_card' : rec.id_card,
                'worked_hours' : worked_hours,
                'pay' : pay,
                'start' : start,
                'end' : end
            }
            row = self.env['empleados.nomina'].search([('id_card','=',rec.id_card),('start','=',start)])
            if worked_hours > 0:
                if row:
                    super(nomina, row).write(vals2)
                else:
                    super(nomina, self).create(vals2)

    employee = fields.Char(string="Empleados")
    id_card = fields.Integer(string="Cedula", group_operator=False)
    start = fields.Date(string="Comienzo del ciclo")
    end = fields.Date(string="Final del ciclo")
    worked_hours = fields.Integer(string="Horas Trabajadas")
    pay = fields.Integer(string="Remuneracion")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
