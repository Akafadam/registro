# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import qrcode
from io import BytesIO
import base64
import random
import string


class productos(models.Model):
    _name = 'productos.productos'

    _sql_constraints = [('products_record', 'UNIQUE(code)',
                         'Este producto ya esta registrado')]

    def get_random_string(self):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(12))
        self.code = result_str

    def validate(self):
        self.state = 'accepted'

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

    @api.onchange('code')
    def create_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
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

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Código", required=True)
    cost = fields.Integer(string="Costo", required=True)
    qr_code = fields.Binary(string="Código QR", required=True,
                            compute="create_qr")

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('accepted', 'Validado')
    ], default="draft")

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
