from odoo import fields, models

from ..controllers import utils


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    nb_equipment = fields.Integer(
        string="Equipements liés à ce partner", compute="_count_equipments"
    )

    def _count_equipments(self):
        for partner in self:
            equipes_list = utils.materiels_equipe_possible_list(self, partner)
            search_domain = [("equipe_id", "in", equipes_list)]
            nb_equipments = self.env["critt.equipment"].search_count(search_domain)
            partner.nb_equipment = nb_equipments
