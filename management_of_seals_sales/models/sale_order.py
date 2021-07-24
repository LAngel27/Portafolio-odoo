# -*- coding: utf-'8' "-*-"

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    seal_photo_mat_line_ids = fields.One2many(
        'carpet.picture.line', 'order_id', string='photos rugs')

    # def action_cancel(self):
    #     res = super(SaleOrder, self).action_cancel()
    #     for record in self:
    #         for line in record.order_line:
    #             for seal in line.seals_ids.ids:
    #                 seal_id = self.env['seal.management'].search(
    #                     [('id', '=', seal)])
    #                 seal_id.update({'state': 'available'})
    #     return res


class CarpetPictures(models.Model):
    _name = 'carpet.picture.line'
    _description = 'model to reference seal with image of the carpet'

    order_id = fields.Many2one('sale.order', string='orden')
    seal_id = fields.Many2one('seal.management', string='Precinto')
    sale_line_id = fields.Many2one(
        'sale.order.line', string='linea del pedido')
    photo_one = fields.Image(
        string='Foto 1', max_width=128, max_height=128, related='seal_id.photo_one', readonly=False)
    photo_two = fields.Image(
        string='Foto 2', max_width=128, max_height=128, related='seal_id.photo_two', readonly=False)
    photo_three = fields.Image(
        string='Foto 3', max_width=128, max_height=128, related='seal_id.photo_three', readonly=False)
    photo_four = fields.Image(
        string='Foto 4', max_width=128, max_height=128, related='seal_id.photo_four', readonly=False)
    photo_five = fields.Image(
        string='Foto 5', max_width=128, max_height=128, related='seal_id.photo_five', readonly=False)
    photo_six = fields.Image(
        string='Foto 6', max_width=128, max_height=128, related='seal_id.photo_six', readonly=False)

    # @api.onchange('photo_one', 'photo_two', 'photo_three', 'photo_four', 'photo_five', 'photo_six')
    # def _onchange_photos(self):
    #     if self.seal_id:
    #         seal = self.env['seal.management'].browse([self.seal_id.id])
    #         seal.write({
    #             'photo_one': self.photo_one if self.photo_one else False,
    #             'photo_two': self.photo_two if self.photo_two else False,
    #             'photo_three': self.photo_three if self.photo_three else False,
    #             'photo_four': self.photo_four if self.photo_four else False,
    #             'photo_five': self.photo_five if self.photo_five else False,
    #             'photo_six': self.photo_six if self.photo_six else False
    #         })
    #     else:
    #         return False
