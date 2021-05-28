# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import qrcode
from io import BytesIO
import base64
import random
import string
# import zbar
# import numpy as np
# import cv2

class productos(models.Model):
    _name = 'inventarios.productos'

    _sql_constraints = [('products_record', 'UNIQUE(code)',
                         'Este producto ya esta registrado')]

    def get_random_string(self):
        # choose from all lowercase letter
        letters = string.ascii_uppercase
        result_str = ''.join(random.choice(letters) for i in range(12))
        # self.code = result_str
        return result_str

    def validate(self):
        self.state = 'accepted'

    def invalidate(self):
        super(productos, self).write({'state': 'draft'})
        # self.state = 'draft'

    @api.model
    def create(self, vals):
        # # print('Hola', self)
        # super(productos, self).write({'code': 'ODNWOJBCJW'})
        # print('Hello')
        vals2 = vals
        vals2['code'] = self.get_random_string()
        return super(productos, self).create(vals2)

    @api.multi
    def unlink(self):
        # data = self[0]
        for rec in self:
            if rec.state == "accepted":
                raise UserError(
                    'El registro fue validado, no puede ser eliminado')
        return super(productos, self).unlink()

    @api.multi
    def write(self, vals):
        if self.state == "accepted":
            raise UserError("El registro fue validado, no puede ser editado")
        return super(productos, self).write(vals)

    def validate(self):
        if self.name:
            pass
        else:
            raise UserError('El campo del nombre está vacio')
        if self.code:
            pass
        else:
            raise UserError('El campo codigo está vacio')
        if self.cost:
            pass
        else:
            raise UserError('El campo de costo está vacio')
        if self.qr_code:
            pass
        else:
            raise UserError('El campo del codigo QR está vacio')
        self.state = 'accepted'

    @api.depends('transactions')
    def _set_units(self):
        default = 0
        # for rec in self.transactions:
        #     if rec.reserve_type == 'ingreso':

    @api.onchange('code')
    @api.depends('code')
    def create_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        data = self[0]
        qr.add_data(data.code)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        data.qr_code = qr_image

    name = fields.Char(string="Nombre")
    code = fields.Char(
        string="Código")
    cost = fields.Integer(string="Costo")
    qr_code = fields.Binary(string="Código QR",
                            compute="create_qr")
    # transactions = fields.One2many('inventarios.inventarios', 'product')
    units = fields.One2many('inventarios.inventarios',
                            'product', string="Unidades")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
