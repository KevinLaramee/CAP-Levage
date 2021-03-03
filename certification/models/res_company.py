# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import odoo


class InheritResCompany(models.Model):
    _inherit = "res.company"
