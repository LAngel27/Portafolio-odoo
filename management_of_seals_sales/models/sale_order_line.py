# -*- coding: utf-'8' "-*-"


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    seals_ids = fields.Many2one('seal.management', string='Precinto',
                                help="El numero de precintos debe ser igual a la cantidad especificada",)

    is_services = fields.Boolean(
        string='indicador de servicio', compute="compute_is_a_service", readonly=False)

    task_id = fields.Many2one('project.task', string='Tarea')
    # seals_ids = fields.Many2many('seal.management', string='Precinto',
    #                              help="El numero de precintos debe ser igual a la cantidad especificada")

    def compute_is_a_service(self):
        for record in self:
            if record.product_id.type == 'service' and record.product_id.service_tracking in ['task_global_project', 'task_in_project']:
                record.is_services = True
            else:
                record.is_services = False

    @api.onchange('product_uom_qty')
    def product_uom_changen(self):
        if self.product_id.type == 'service' and self.product_id.service_tracking in ['task_global_project', 'task_in_project']:
            if self.task_id:
                if self.product_uom_qty > 1 or self.product_uom_qty == 1:
                    self.product_uom_qty = 1
                    self.is_services = True
                else:
                    self.product_uom_qty = 0
                    self.is_services = False
            else:
                self.task_id = False
                self.product_uom_qty = 1

    @api.onchange('seals_ids')
    def _onchange_seals_ids(self):
        for record in self:
            seal = self.env['seal.management'].search(
                [('id', '=', record.seals_ids.id)])
            line_photo_rug = self.env['carpet.picture.line'].search(
                [('sale_line_id.id', '=', self._origin.id)])
            if record.order_id and record.seals_ids:
                record.product_uom_qty = 1
                order = self.env['sale.order'].search(
                    [('name', '=', record.order_id.name)])
                seal.write(
                    {'state': 'used', 'partner_id': record.order_id.partner_id.id, 'sale_order_id': order.id})
                if line_photo_rug:
                    photos = dict(
                        photo_one=line_photo_rug.photo_one,
                        photo_two=line_photo_rug.photo_two,
                        photo_three=line_photo_rug.photo_three,
                        photo_four=line_photo_rug.photo_four,
                        photo_five=line_photo_rug.photo_five,
                        photo_six=line_photo_rug.photo_six)
                    seal.update(photos)
                    if line_photo_rug.seal_id.name != record.seals_ids.name:
                        seal_write = self.env['seal.management'].search(
                            [('id', '=',  line_photo_rug.seal_id.id)])
                        photos_false = dict(
                            photo_one=False, photo_two=False, photo_three=False, photo_four=False, photo_five=False, photo_six=False)
                        if seal_write:
                            seal_write.write(
                                {'state': 'available', 'partner_id': False, 'sale_order_id': False, **photos_false})
                        else:
                            seal_write = False
                        line_photo_rug.update({
                            'seal_id': seal.id if seal.id else False
                        })
                        record.seals_ids = seal.id
                else:
                    if order:
                        vals = {
                            'order_id': order.id,
                            'seal_id': record.seals_ids.id,
                            'sale_line_id': self.id.origin
                        }
                        self.env['carpet.picture.line'].create(vals)
                    else:
                        order = False
            else:
                if line_photo_rug:
                    if line_photo_rug.seal_id.name != record.seals_ids.name:
                        seal_write = self.env['seal.management'].search(
                            [('id', '=',  line_photo_rug.seal_id.id)])
                        task = self.env['project.task'].search(
                            [('seal_id.id', '=', seal_write.id)])
                        photos_false = dict(
                            photo_one=False, photo_two=False, photo_three=False, photo_four=False, photo_five=False, photo_six=False)
                        if task:
                            record.seals_ids = seal_write.id
                            raise UserError(
                                _(f'El precinto {seal_write.name} tiene una tarea asociada {task.name} si desea eliminar la tarea coloque la cantidad en 0'))
                        else:
                            seal_write.update({'state': 'available', 'state': 'available',
                                              'partner_id': False, 'sale_order_id': False, **photos_false})
                        line_photo_rug.update({
                            'seal_id': record.seals_ids.id
                        })
            if record.task_id:
                task = self.env['project.task'].search(
                    [('id', '=', record.task_id.id)])
                if task.seal_id.name != record.seals_ids.name:
                    seal_write = self.env['seal.management'].search(
                        [('id', '=',  task.seal_id.id)])
                    if seal_write:
                        seal_write.update({
                            'state': 'available'
                        })
                    else:
                        seal_write = False
                    task.update({
                        'seal_id': record.seals_ids.id if record.seals_ids else False
                    })
            else:
                pass

    def _timesheet_create_task_prepare_values(self, project):
        self.ensure_one()
        planned_hours = self._convert_qty_company_hours(self.company_id)
        sale_line_name_parts = self.name.split('\n')
        title = sale_line_name_parts[0] or self.product_id.name
        description = '<br/>'.join(sale_line_name_parts[1:])
        seal = self.env['sale.order.line'].search([('id', '=', self.id)])
        return {
            'name': title if project.sale_line_id else '%s: %s' % (self.order_id.name or '', title),
            'planned_hours': planned_hours,
            'partner_id': self.order_id.partner_id.id,
            'email_from': self.order_id.partner_id.email,
            'description': description,
            'project_id': project.id,
            'sale_line_id': self.id,
            'sale_order_id': self.order_id.id,
            'company_id': project.company_id.id,
            'seal_id': seal.seals_ids.id,
            'user_id': False,  # force non assigned task, as created as sudo()
        }

    def write(self, values):
        res = super().write(values)
        self.ensure_one()
        if values.get('product_uom_qty', False) == 0:
            if self.task_id:
                if self.product_uom_qty < 1 and self.qty_invoiced < 1:
                    task = self.env['project.task'].browse(
                        [self.task_id.id])
                    photos_false = dict(
                        photo_one=False, photo_two=False, photo_three=False, photo_four=False, photo_five=False, photo_six=False)
                    task.write(
                        {'sale_order_id': False, 'sale_line_id': False})
                    seal = task.seal_id
                    seal_write = self.env['seal.management'].browse([seal.id])
                    seal_write.write(
                        {'state': 'available', 'partner_id': False, 'sale_order_id': False, **photos_false})
                    task.unlink()
                    self.seals_ids = False
                    photo_rug = self.env['carpet.picture.line'].search(
                        [('seal_id.id', '=', seal.id)])
                    photo_rug.unlink()
                else:
                    self.product_uom_qty = 1
        else:
            if not self.task_id and values.get('product_uom_qty', False) == 1:
                project_id = self.product_id.project_id.id
                if project_id:
                    project = self.env['project.project'].browse(
                        [project_id])
                    vals = self._timesheet_create_task_prepare_values(
                        project)
                else:
                    project_id = False
                if self.seals_ids:
                    seal = {'seal_id': self.seals_ids.id}
                    values_create = dict(vals, **seal)
                    task = self.env['project.task'].create(
                        values_create)
                    self.task_id = task.id
                else:
                    self.seals_ids = False
        return res

        # @api.onchange('seals_id')
        # def _onchange_seals_ids(self):
        #     for record in self:
        #         if record.product_uom_qty and record.seals_ids.ids:
        #             if len(record.seals_ids.ids) > int(record.product_uom_qty):
        #                 raise UserError(_(
        #                     'El numero de precintos debe ser igual a la cantidad especificada'))
        #             for order in record.order_id:
        #                 if order.state == 'sale':
        #                     for seal in record.seals_ids.ids:
        #                         seal_id = self.env['seal.management'].search(
        #                             [('id', '=', seal)])
        #                         seal_id.update({'state': 'used'})
        #                 else:
        #                     for seal in record.seals_ids.ids:
        #                         seal_id = self.env['seal.management'].search(
        #                             [('id', '=', seal)])
        #                         seal_id.update({'state': 'available'})
        #         else:
        #             pass

        # def unlink(self):
        #     if self._check_line_unlink():
        #         raise UserError(
        #             _('You can not remove an order line once the sales order is confirmed.\nYou should rather set the quantity to 0.'))
        #     for record in self:
        #         for seal in record.seals_ids.ids:
        #             seal_id = self.env['seal.management'].search(
        #                 [('id', '=', seal)])
        #             seal_id.update({'state': 'available'})
        #     return super(SaleOrderLine, self).unlink()

        # def write(self, values):
        #     res = super(SaleOrderLine, self).write(values)
        #     for record in self:
        #         if not int(record.product_uom_qty) == len(record.seals_ids.ids):
        #             raise UserError(_(
        #                 'El numero de precintos debe ser igual a la cantidad especificada'))
        #     return res

        # @api.onchange('product_uom_qty')
        # def _onchange_validator(self):
        #     for record in self:
        #         if int(record.product_uom_qty) and len(record.seals_ids.ids):
        #             if len(record.seals_ids.ids) < int(record.product_uom_qty):
        #                 result = int(record.product_uom_qty) - \
        #                     len(record.seals_ids.ids)
        #                 warning = {
        #                     'title': _('Aviso'),
        #                     'message': _(f'Le falta seleccionar {result} {"precintos" if result > 1 else "precinto"}.')
        #                 }
        #                 return {'warning': warning}
        #             elif len(record.seals_ids.ids) > int(record.product_uom_qty):
        #                 record.product_uom_qty = float(len(record.seals_ids.ids))
        #                 warning = {
        #                     'title': _('Warning'),
        #                     'message': _('El numero de precintos debe ser igual a la cantidad especificada')
        #                 }
        #                 return {'warning': warning}
