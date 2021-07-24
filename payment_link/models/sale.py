from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # def _default_payment_icon(self):
    #     icon = self.env.ref('payment_link.payment_icon_webpay').id
    #     return icon

    payment_icon_id = fields.Many2one(
        'payment.icon', string='Icono de Pago')  # default=_default_payment_icon)
