# -*- coding: utf-'8' "-*-"

from odoo.exceptions import UserError
from odoo import _, api, fields, models


class SealManagement(models.Model):
    _name = 'seal.management'
    _description = 'management of seals'

    name = fields.Char(string='Numero')
    partner_id = fields.Many2one('res.partner', string='Cliente')
    sale_order_id = fields.Many2one('sale.order', string='Orden de trabajo')
    photo_one = fields.Image(string='Foto 1', max_width=128, max_height=128)
    photo_two = fields.Image(string='Foto 2', max_width=128, max_height=128)
    photo_three = fields.Image(string='Foto 3', max_width=128, max_height=128)
    photo_four = fields.Image(string='Foto 4', max_width=128, max_height=128)
    photo_five = fields.Image(string='Foto 5', max_width=128, max_height=128)
    photo_six = fields.Image(string='Foto 6', max_width=128, max_height=128)
    state = fields.Selection(string='Estado', selection=[
                            ('available', 'Disponible'), ('used', 'Usado')], default='available')

    def unlink(self):
        for record in self:
            if record.state == 'used':
                raise UserError('No puede eliminar precintos en estado usado')
        return super(SealManagement, self).unlink()

    def reset_available(self):
        task = self.env['project.task'].search(
            [('seal_id.id', '=', self.id)])
        if task:
            raise UserError(
                _(f'Cambio de estado no valido!,este precinto pertenece a la tarea {task.name}'))
        else:
            self.state = 'available'
