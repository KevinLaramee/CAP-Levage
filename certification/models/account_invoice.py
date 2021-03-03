import logging

from ast import literal_eval

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import ustr

from odoo.addons.base.ir.ir_mail_server import MailDeliveryException
from odoo.addons.auth_signup.models.res_partner import SignupError, now
from datetime import datetime


class AccountInvoiceInherit(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        res = super(AccountInvoiceInherit, self).create(vals)

        sale_order = self.env["sale.order"].search([("name", "=", res.origin)])
        if sale_order:
            for equipment in sale_order.order_line_equipment:
                equipment.equipment_id.write(
                    {"derniere_facture": res.id, "num_derniere_facture": res.number}
                )

        return res

    @api.multi
    def write(self, vals):
        res = super(AccountInvoiceInherit, self).write(vals)

        sale_order = self.env["sale.order"].search([("name", "=", self.origin)])
        if sale_order:
            for equipment in sale_order.order_line_equipment:
                equipment.equipment_id.write(
                    {"derniere_facture": self.id, "num_derniere_facture": self.number}
                )

        return res
