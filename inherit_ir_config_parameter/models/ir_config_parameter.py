# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    def _time_corection_expiration_db(self):
        ir_config_date_expire = self.sudo().search(
            [('key', '=', 'database.expiration_date')])
        if ir_config_date_expire:
            date_expired = ir_config_date_expire.value
            date = datetime.strptime(date_expired, '%Y-%m-%d %H:%M:%S')
            date_end = date + timedelta(days=1)
            ir_config_date_expire.sudo().update({'value': str(date_end)})
        else:
            return False
