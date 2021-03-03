from odoo import api, models, fields, tools
from odoo.tools import pycompat
from datetime import time, datetime, date
import os


class inherit_repair(models.Model):
    _name = "repair.order"
    _inherit = "repair.order"

    # product_id = fields.Many2one(
    #    'product.product', string='Product to Repair',
    #    readonly=True, required=False, states={'draft': [('readonly', False)]})

    product_id = fields.Many2one(
        "product.product",
        string="Product to Repair",
        readonly=True,
        required=False,
        states={"draft": [("readonly", False)]},
    )

    equipment_id = fields.Many2one(
        "critt.equipment",
        string="Matériel à réparer",
        required=True,
        domain="[('res_partner_id', '=', partner_id)]",
    )
