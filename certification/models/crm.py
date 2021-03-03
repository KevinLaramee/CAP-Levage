# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import odoo


class InheritCRMLead(models.Model):
    _inherit = "crm.lead"


class InheritCRMTeam(models.Model):
    _inherit = "crm.team"


class InheritCRMActivityReport(models.Model):
    _inherit = "crm.activity.report"


class InheritCRMLeadTag(models.Model):
    _inherit = "crm.lead.tag"


class InheritCRMLeadScoringFrequencyField(models.Model):
    _inherit = "crm.lead.scoring.frequency.field"


class InheritCRMLeadScoringFrequency(models.Model):
    _inherit = "crm.lead.scoring.frequency"


class InheritCRMLostReason(models.Model):
    _inherit = "crm.lost.reason"


class InheritCRMStage(models.Model):
    _inherit = "crm.stage"
