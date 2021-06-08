from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
import calendar

time = [
    (0, '00:00'),
    (1, '01:00'),
    (2, '02:00'),
    (3, '03:00'),
    (4, '04:00'),
    (5, '05:00'),
    (6, '06:00'),
    (7, '07:00'),
    (8, '08:00'),
    (9, '09:00'),
    (10, '10:00'),
    (11, '11:00'),
    (12, '12:00'),
    (13, '13:00'),
    (14, '14:00'),
    (15, '15:00'),
    (16, '16:00'),
    (17, '17:00'),
    (18, '18:00'),
    (19, '19:00'),
    (20, '20:00'),
    (21, '21:00'),
    (22, '22:00'),
    (23, '22:00')
]


class asistencias(models.Model):
    _name = 'empleados.asistencias'

    _sql_constraints = [
        ('charge_record_constrain', 'UNIQUE(name)', 'Este cargo ya está registrado')
    ]

    def validate(self):
        if self.employee:
            pass
        else:
            raise UserError('No se ha especificado al empleado')
        if self.date:
            pass
        else:
            raise UserError('No se ha especificado la fecha')
        if self.arrive_time:
            pass
        else:
            raise UserError('No se ha especificado la hora de entrada')
        if self.leave_time:
            pass
        else:
            raise UserError('No se ha especificado la hora de salida')
        self._check_date()
        self.state = 'accepted'

    @api.multi
    def unlink(self):
        # data = self[0]
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(asistencias, self).unlink()

    def _check_date(self):
        for rec in self.env['empleados.asistencias'].search([]):
            if self.env['empleados.asistencias'].search([('date','=', rec.date),('state','=','accepted'),('employee','=',self.employee.id)]):
                # print(self.env['citas.personas'].search([('id_card','=', self.id_card)]).name)
                raise UserError('Esta fecha ya esta registrada')

    def _last_day(self, year, month):
        last_day = calendar.monthrange(year, month)[1]
        print('\033[94m' + f"{last_day}")
        return date(year, month, last_day)

   # def _mid_day(self, year, month):
   #     date = datetime.date.today()
   #     return date.replace(month=month, year=year, day=15)
   #	
   # def _first_day(self, year, month):
   #     date = datetime.date.today()
   #     return date.replace(month=month, year=year, day=1)

    @api.constrains('date')
    def _check_interval(self):
        current_year = date.today().year
        current_month = date.today().month
        if  date.today() < date(current_year, current_month, 15):
            print('\033[94m' + f'{current_year}')
            print('\033[91m' + f'{current_month}')
            print('\033[93m' + f'{self.date.today()}')
            if self.date < self._last_day(current_year, current_month - 1):
                raise UserError('La fecha es inferior al intervalo')
            if self.date > date(current_year, current_month, 15):
                raise UserError('La fecha es superior al intervalo')
        if date.today() >= date(current_year, current_month, 15):
            if self.date < date(current_year, current_month, 15):
                raise UserError('La fecha es inferior al intervalo')
            if self.date > self._last_day(current_year, current_month):
                raise UserError('La fecha es superior al intervalo')

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(asistencias, self).write(vals)

    def invalidate(self):
        super(asistencias, self).write({'state': 'draft'})

    def calculate_hours(self, arrive, leave):
        result = 0
        if arrive and leave:
            if arrive > leave:
                raise UserError('La hora de entrada no puede ser mayor a la de salida')
            result = leave - arrive
        else:
            result = 0
        return result

    @api.onchange('arrive_time', 'leave_time', 'employee', 'date')
    @api.depends('arrive_time', 'leave_time', 'employee', 'date')
    def _set_pay(self):
        for rec in self:
            unit = 100
            extra_hours = 0
            pay = 0
            actual_worked = 0
            expected_worked = 0
            if isinstance(rec.arrive_time, int) and isinstance(rec.leave_time, int):
                actual_worked = self.calculate_hours(rec.arrive_time, rec.leave_time)
            if isinstance(rec.employee.schedule.arrive_time, int) and isinstance(rec.employee.schedule.leave_time, int):
                expected_worked = self.calculate_hours(rec.employee.schedule.arrive_time, rec.employee.schedule.leave_time)
            if actual_worked > expected_worked:
                extra_hours = actual_worked - expected_worked
            if actual_worked and expected_worked:
                print('Hola')
                pay = (actual_worked - extra_hours) * unit + extra_hours * unit * 1.5
            rec.pay = pay
            rec.worked_hours = actual_worked

    employee = fields.Many2one('empleados.empleados', string="Empleado")
    date = fields.Date(string="Fecha")
    arrive_time = fields.Selection(time, string="Hora de llegada")
    leave_time = fields.Selection(time, string="Hora de salida")
    pay = fields.Integer()
    # expected_worked_hours = fields.Integer()
    worked_hours = fields.Integer()
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
