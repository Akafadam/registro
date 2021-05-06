# -*- coding: utf-8 -*-

from odoo import models, fields, api
import qrcode

class productos(models.Model):
    _name = 'productos.productos'

    @api.depends('qr_code')
    def create_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        img = qr.make_image("HOla que hace")
        img.save('home/tecnoparaguana/qr.jpg')

    name = fields.Char(string="Nombre", required=True)
    code = fields.Integer(string="Código", required=True)
    cost = fields.Integer(string="Costo", required=True)
    qr_code = fields.Binary(string="Código QR", required=True, compute="create_qr", attachment=True)

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100