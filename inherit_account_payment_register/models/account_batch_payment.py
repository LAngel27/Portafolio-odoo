# -*- coding: utf-8 -*-

from odoo import fields, models, api
from io import BytesIO
from datetime import datetime 
import base64
import xlwt
import re


class AccountBacthPayment(models.Model):
    _inherit = 'account.batch.payment'

    def get_report_xlsx(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet('banco')
        today = datetime.now().date()
        center = xlwt.easyxf('align: horiz centre')
        file_name = 'Extracto bancario' + str(today)
        sheet.write(0, 0,'Cta_origen',center)
        sheet.write(0, 1,'Moneda',center)
        sheet.write(0, 2,'Cta_destino',center)
        sheet.write(0, 3,'Moneda_destino', center)
        sheet.write(0, 4,'Cod_banco',center)
        sheet.write(0, 5,'RUT benef.',center)
        sheet.write(0, 6, 'Nombre benef.', center)
        sheet.write(0, 7, 'Mto total', center)
        sheet.write(0, 8, 'Glosa TEF', center)
        sheet.write(0, 9, 'Correo', center)
        sheet.write(0, 10,'Glosa Correo', center)
        sheet.write(0, 11,'Glosa Cartola cliente', center)
        sheet.write(0, 12,'Glosa Cartola Beneficiario', center)
        line = 0
        for vals in self.payment_ids:
            acc_number = ''
            bank_id = ''
            email = vals.partner_id.email or ''
            for values in vals.partner_id.bank_ids:
                acc_number = values.acc_number
                bank_id = values.bank_id.l10n_cl_sbif_code
            line += 1
            sheet.write(line, 0, vals.batch_payment_id.journal_id.bank_account_id.acc_number)
            sheet.write(line, 1, vals.currency_id.name)
            sheet.write(line, 2, acc_number)
            sheet.write(line, 3, vals.currency_id.name)
            sheet.write(line, 4, bank_id)
            partner_id_vat = vals.partner_id.vat
            x = re.sub('[-.]', '', partner_id_vat)
            sheet.write(line, 5, x)
            sheet.write(line, 6, vals.partner_id.name)
            sheet.write(line, 7, vals.amount)
            sheet.write(line, 8, f'{vals.partner_id.name} {vals.ref}')
            sheet.write(line, 9, email)
            sheet.write(line, 10, f'{vals.company_id.name} {vals.ref}')
            
            c = re.sub('[-.]', '', vals.partner_id.vat)
            a = f'{c} {vals.partner_id.name}'
            if len(a) > 20:
                a = a[0:20]
                
            sheet.write(line, 11, a)
            d = re.sub('[-.]', '', vals.company_id.vat)
            b = f'{d} {vals.company_id.name}'
            if len(b) > 20:
                b = b[0:20]
            sheet.write(line, 12, b)

            


        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        data_b64 = base64.encodestring(data)
        doc = self.env['ir.attachment'].create({
            'name': '%s.xls' % (file_name),
            'datas': data_b64,
            'store_fname': '%s.xls' % (file_name),
            'type': 'url'
        })
        return {
            'type': "ir.actions.act_url",
            'url': "web/content/?model=ir.attachment&id=" + str(
                doc.id) + "&filename_field=name&field=datas&download=true&filename=" + str(doc.name),
            'target': "current",
        }
