# -*- coding: utf-8 -*-

import time, datetime
import logging
import re
import uuid
from odoo import models, fields, api, exceptions, _
from odoo.addons.http_routing.models.ir_http import slug
from werkzeug import urls
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import odoo
import base64

_logger = logging.getLogger(__name__)


class Planification(models.Model):
    _name = "critt.certification.planification"
    _rec_name = "client"
    _order = "date"

    client = fields.Many2one(
        "res.partner",
        "Client",
        required=True,
        domain=[("customer", "=", "true"), ("is_company", "=", False)],
    )

    date = fields.Datetime(string="Date du contrôle", copy=True, required=True)
    fin = fields.Datetime(string="Fin de l'audit", copy=True, required=True)
