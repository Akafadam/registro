# -*- coding: utf-8 -*-
from odoo import models, fields, api
import qrcode
from io import BytesIO
import base64


class productos(models.Model):
    _name = 'productos.productos'

    _sql_constraints = [('products_record','UNIQUE(code)', 'Este producto ya esta registrado')]

    @api.onchange('code')
    def create_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.code)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_code = qr_image

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Código", required=True)
    cost = fields.Integer(string="Costo", required=True)
    qr_code = fields.Binary(string="Código QR", required=True,
                            compute="create_qr", attachment=True)

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
