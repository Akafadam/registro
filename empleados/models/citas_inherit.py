# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import re
from odoo.exceptions import UserError, ValidationError

class citas(models.Model):
    _inherit = 'citas.citas'

    medic_id = fields.Many2one(
        comodel_name='empleados.empleados', string="Medico", domain="[('is_medic','=',True)]")