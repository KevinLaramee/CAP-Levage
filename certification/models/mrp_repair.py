from odoo import api, models, fields, tools
from odoo.tools import pycompat
from datetime import time, datetime, date
import os


class inherit_mrp_repair(models.Model):
    _name = "mrp.repair"
    _inherit = "mrp.repair"

    # product_id = fields.Many2one(
    #    'product.product', string='Product to Repair',
    #    readonly=True, required=False, states={'draft': [('readonly', False)]})
