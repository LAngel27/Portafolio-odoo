# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    retire = fields.Boolean(string='Retiro')

