# -*- coding: utf-8 -*-
from odoo import fields, models, api



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine,self).product_id_change()
        for record in self:
            if record.product_id.retire:
                record.discount = 100
        return res
