# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    number_check = fields.Integer(string='Numero de cheque')
    check_name = fields.Char(string='Nombre del cheque')
    check_date_start = fields.Date(string='Fecha de emision del cheque')
    check_date_payment = fields.Date(string='Fecha de pago del cheque')
    check_cuit = fields.Char(string='CUIT del propietario del cheque')
    name_propietary_check = fields.Char(string='Nombre del propietario del cheque')
    code = fields.Char(string='Codigo')
    invoice_id = fields.Many2one('account.move', 'Factura')
