# -*- coding: utf-'8' "-*-"

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import pandas as pd


class SequenceCreator(models.TransientModel):
    _name = 'sequence.creator'

    number_start = fields.Integer(string='Nro. Inicial')
    number_end = fields.Integer(string='Nro. Final')
    sequence_size = fields.Integer(string='Tamaño de secuencia')

    def create_sequence(self):
        if self.number_start > self.number_end:
            raise UserError(
                _('El Nro. inicial no puede ser mayor al Nro. final'))
        else:
            seal_management_ids = self.env['seal.management'].search([])
            if seal_management_ids:
                seals = seal_management_ids.mapped('name')
                seals_no_creates = []
                start_item = int(seal_management_ids[0].name)
                end_item = int(seal_management_ids[-1].name)
                #seals = [seq for seq in range(start_item, end_item + 1)]
                # if self.number_start in seals or seals[-1] == self.number_start or seals[-1] == self.number_end:
                #     # in case the sequence repeat
                #     raise UserError(
                #         _(f'Ya hay un numero de secuencia generado en ese rango establecido intente con {end_item + 1} como Nro. inicial'))
                for seq in range(self.number_start, self.number_end + 1):
                    if str(seq).zfill(self.sequence_size) not in seals:
                        vals = dict(
                            name=str(seq).zfill(self.sequence_size),
                            state='available'
                        )
                        self.env['seal.management'].create(vals)
                    else:
                        seals_no_creates.append(
                            str(seq).zfill(self.sequence_size))
                if seals_no_creates:
                    raise UserError(
                        _("Los siguientes {} precintos ya existen: \n {} \n Corrija por favor la secuencia").format(len(seals_no_creates), seals_no_creates))
            else:
                for seq in range(self.number_start, self.number_end + 1):
                    vals = dict(
                        name=str(seq).zfill(self.sequence_size),
                        state='available'
                    )
                    self.env['seal.management'].create(vals)
