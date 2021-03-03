# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import odoo


class InheritProductProduct(models.Model):
    _inherit = "product.product"
