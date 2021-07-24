from odoo import api, fields, models, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    move_id = fields.Many2one(comodel_name='account.move', string='Factura', compute='_compute_sale_order_id')

    def _compute_sale_order_id(self):
        for task in self:
            move_obj = self.env['account.move']
            if task.sale_order_id:
                move = move_obj.search([('invoice_origin', '=', task.sale_order_id.name),('payment_state', 'in', ['not_paid', 'partial'])], limit=1)
                if move:
                    task.move_id = move.id
                else:
                    task.move_id = False
            else:
                task.move_id = False
