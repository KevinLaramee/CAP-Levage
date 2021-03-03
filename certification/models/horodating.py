import datetime
from odoo import api, models, fields, tools, _
from datetime import time, datetime, date, timedelta


class Horodating(models.Model):
    _name = "critt.horodating"
    _order = "create_date desc"

    action = fields.Char(string="Action réalisée")
    user = fields.Many2one("res.users", string="Utilisateur")

    equipment_id = fields.Many2one("critt.equipment", string="Id Matériel")
