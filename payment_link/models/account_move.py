from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import ustr, consteq, float_compare
import hashlib
import hmac
from odoo.tools.misc import get_lang

from werkzeug import urls


class AccountMove(models.Model):
    _inherit = 'account.move'

    # def _default_payment_icon(self):
    #     icon = self.env.ref('payment_link.payment_icon_webpay').id
    #     return icon

    link = fields.Char(string='Payment Link')
    payment_icon_id = fields.Many2one(
        'payment.icon', string='Icono de Pago')  # default=_default_payment_icon)

    def link_payment(self):
        # secret = self.env['ir.config_parameter'].sudo().get_param('database.secret')
        # token_str = '%s%s%s' % (self.partner_id.id, self.amount_total, self.currency_id.id)
        # access_token = hmac.new(secret.encode('utf-8'), token_str.encode('utf-8'), hashlib.sha256).hexdigest()
        for rec in self:
            if rec.payment_reference:
                name = rec.payment_reference
            else:
                raise UserError('Por favor ingrese una referencia de pago')
            #wzd = self.env.ref('payment.action_invoice_order_generate_link').sudo().read()[0]
            context = {
                'active_id': rec.id,
                'active_model': rec._name
            }
            vals = {
                'amount': rec.amount_residual,
                'currency_id': rec.currency_id.id,
                'partner_id': rec.partner_id.id,
                'description': name
            }
            PaymentLink = self.env['payment.link.wizard']
            payment_link_obj = PaymentLink.with_context(
                active_id=rec.id, active_model=rec._name).create(vals)
            link = payment_link_obj.link
            rec.update({'link': link})

        # def check_token(self, access_token, partner_id, amount, currency_id):
        #     secret = self.env['ir.config_parameter'].sudo().get_param('database.secret')
        #     token_str = '%s%s%s' % (partner_id, amount, currency_id)
        #     correct_token = hmac.new(secret.encode('utf-8'), token_str.encode('utf-8'), hashlib.sha256).hexdigest()
        #     if consteq(ustr(access_token), correct_token):
        #         return True
        #     return False

    def action_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        self.link_payment()
        template = self.env.ref(
            'payment_link.email_template_edi_invoice_inh', raise_if_not_found=False)
        lang = False
        if template:
            lang = template._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref(
            'account.account_invoice_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects.
            default_res_model='account.move',
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
