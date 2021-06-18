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
    speciality = fields.Many2one(
        comodel_name='empleados.especialidad', string="Especialidad Medica")

    # @api.depends('search_by')
    @api.onchange('search_by', 'speciality')
    def set_domain_for_teacher(self): 
        print('\033[91m' + f'{self.search_by}') 
        if self.search_by == 'especialidad':
            class_obj = self.env['empleados.empleados'].search(
                [('speciality', '=', self.speciality.id)])
            speciality_list = []
            for data in class_obj:
                speciality_list.append(data.id)

            res = {}
            res['domain'] = {'medic_id': [
                ('id', 'in', speciality_list), ('state', '=', 'accepted')]}
            return res
        else:
            res = {}
            res['domain'] = {'medic_id': [
                ('state', '=', 'accepted'), ('is_medic', '=', True)]}
            return res

    @api.onchange('speciality')
    def _clean_medic_data(self):
        for rec in self:
            if rec.search_by == 'especialidad':
                rec.medic_id = False

    @api.onchange('medic_id')
    @api.depends('medic_id')
    def _set_specs(self):
        for rec in self:
            if rec.search_by == 'medico':
                rec.speciality = rec.medic_id.speciality
                rec.speciality = rec.medic_id.speciality