# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models





class InhProductTemplate(models.Model):
    _inherit = 'product.template'

    name_english = fields.Char(string='Nombre en ingles')
    replace_code = fields.Char(string='Codigo de reemplazo')
    stock_ubication = fields.Char(string='Ubicacion en Bodega')