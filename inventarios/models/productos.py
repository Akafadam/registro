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

    # def get_random_string(self):
    #     letters = string.ascii_uppercase
    #     result_str = ''.join(random.choice(letters) for i in range(12))
    #     return result_s

    def get_code(self):
        arg = []
        items = None
        # product_code = f"item-#{len(self.env['inventarios.productos'].search([('state','=','accepted')])) + num}"
        if self.env['inventarios.productos'].search([('state','=','accepted')]):
            items = self.env['inventarios.productos'].search([('state','=','accepted')])
            for p in items:
                arg.append(p.create_date)
            last =  max(arg)
            item_result = self.env['inventarios.productos'].search([('create_date','=',last)])
            next = int(item_result.code.split('#')[1])
            return f'item-#{next + 1}'
        else:
            return f'item-#1'


        
        print(max(arg))
        raise UserError('Stop')
        # while(self.env['inventarios.productos'].search([('code', '=', product_code)])):
        #     num += 1
        #     product_code = f"item-#000{len(self.env['inventarios.productos'].search([('state','=','accepted')])) + num}"
        # return product_code

    # def validate(self):
    #     self.code = self.get_code()
    #     self.state = 'accepted'

    def invalidate(self):
        for item in self.transactions:
            if item.state == 'accepted':
                raise UserError("Este registro no puede ser invalidado, ya que está referenciado en otro registro validado")
        super(productos, self).write({'state': 'draft'})
        # self.state = 'draft'

    # @api.model
    # def create(self, vals):
    #     # # print('Hola', self)
    #     # super(productos, self).write({'code': 'ODNWOJBCJW'})
    #     # print('Hello')
    #     vals2 = vals
    #     vals2['code'] = product_code
    #     return super(productos, self).create(vals2)

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
        self.code = self.get_code()
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

    # @api.depends('transactions')
    # def _set_units(self):
    #     default = 0
    #     # for rec in self.transactions:
    #     #     if rec.reserve_type == 'ingreso':

    @api.depends('table')
    @api.onchange('table')
    @api.multi
    def _set_units(self):
        total = 0
        for record in self:
            for rec in record.table:
                if rec.reserve_type == 'ingreso':
                    total += rec.cuantity
                if rec.reserve_type == 'egreso':
                    total -= rec.cuantity
            record.units = total

    @api.onchange('code')
    @api.depends('code')
    def create_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        for data in self:
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
    transactions = fields.One2many('inventarios.inventarios', 'product')
    table = fields.One2many('inventarios.inventarios',
                            'product', domain=[('state', '=', 'accepted')])
    units = fields.Integer(string="Unidades", readonly=True, compute="_set_units")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
