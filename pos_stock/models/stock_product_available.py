from odoo import api, fields, models 

class StockProdcutAvailable(models.Model):
    _name = 'stock.product.available'
    _description = 'Stock Prodcut Available'

    product_tmpl_id = fields.Many2one('product.template', 'Producto')
    product_id = fields.Many2one('product.product', 'Producto')
    location_id = fields.Many2one('stock.location', 'Ubicacion')
    quantity = fields.Float('Cantidad')

    
