from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

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


class horario(models.Model):
    _name = 'empleados.horario'

    _sql_constraints = [
        ('charge_record_constrain', 'UNIQUE(name)', 'Este cargo ya está registrado')
    ]

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(horario, self).unlink()

    @api.depends('arrive_time', 'leave_time')
    @api.multi
    def _set_interval(self):
        for rec in self:
            rec.interval = f"{rec.arrive_time}:00-{rec.leave_time}:00"

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(horario, self).write(vals)

    def validate(self):
        if self.arrive_time:
            pass
        else:
            raise UserError('No se ha especificado la hora de entrada')
        if self.leave_time:
            pass
        else:
            raise UserError('No se ha especificado la hora de salida')
        self.state = 'accepted'

    def invalidate(self):
        super(horario, self).write({'state': 'draft'})

    # employee = fields.Many2one('empleados.empleados', string="Empleados")
    _rec_name = 'interval'
    arrive_time = fields.Selection(time, string="Hora de llegada")
    leave_time = fields.Selection(time, string="Hora de salida")
    interval = fields.Char(compute="_set_interval")
    button_visible = fields.Boolean(default=True)

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")
