# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    show_stock_product = fields.Boolean('Mostrar stock de productos')
    show_stock_product_none = fields.Boolean(
        'No mostrar productos con stock en 0')
    lock_stock_product = fields.Boolean('Bloquear si no hay stock')
    # warehouse_id = fields.Many2one('stock.warehouse', 'Almacen por defecto')
    # location_id = fields.Many2one(
    #     'stock.location', string='Ubicacion por defecto')

    warehouse_ids = fields.Many2many(
        'stock.warehouse', string='Almacenes disponibles')
    location_ids = fields.Many2many(
        'stock.location', string='Ubicaciones disponibles')
    warehouse_change = fields.Char(string='Cambio bodega')
