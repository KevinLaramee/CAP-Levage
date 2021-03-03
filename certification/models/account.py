# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import odoo


class InheritAccountTax(models.Model):
    _inherit = "account.tax"


class InheritAccountTaxGroup(models.Model):
    _inherit = "account.tax.group"
