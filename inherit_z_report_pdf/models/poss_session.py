# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime


class PossSessionInherit(models.Model):
    _inherit = 'pos.session'

    def get_seller_for_poss(self):
        if self.state == 'closed':
            seller = []
            date_post = datetime.datetime.strftime(self.start_at, '%Y-%m-%d')
            seller_ids = self.env['pos.order'].search(
                [('session_id.id', '=', self.id)])
            for line in seller_ids:
                if datetime.datetime.strftime(line.date_order, '%Y-%m-%d') == date_post:
                    seller.append(line.user_id.name)
            return seller
        else:
            return False
