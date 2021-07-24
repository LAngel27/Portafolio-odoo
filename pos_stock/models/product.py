from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def calculate_qty_sale_available(self, config):
        warehouse_id = self.env['pos.config'].search(
            [('id', '=', config)]).picking_type_id.warehouse_id
        product_id = self.search([('id', '=', self.id)])
        qty_sale_available = sum(product_id.stock_quant_ids.filtered(
            lambda q: q.location_id == warehouse_id.lot_stock_id).mapped('available_quantity'))
        return qty_sale_available
