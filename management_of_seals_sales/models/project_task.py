from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    seal_id = fields.Many2one('seal.management', string='Precinto')

    # seals_ids = fields.Many2one(
    #     'seal.management', string='Precintos', related='sale_line_id.seals', readonly=False)