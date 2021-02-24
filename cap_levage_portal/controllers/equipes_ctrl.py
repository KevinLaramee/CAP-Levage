# -*- coding: utf-8 -*-
from cap_levage_portal.controllers.abstract_equipes_agences_ctrl import (
    AbstractEquipesagencesCtrl,
)
from odoo import http

from odoo.tools.translate import _

class CapLevageEquipes(AbstractEquipesagencesCtrl, http.Controller):
    @http.route(
        [
            "/cap_levage_portal/equipes",
            "/cap_levage_portal/equipes/page/<int:page>",
        ],
        auth="user",
        website=True,
    )
    def equipes_list(self, page=1, sortby="name", search=None, search_in="allid", **kw):
        """
        Page affichange une liste de matériels.
        :param search_in: ou rechercher
        :param page: page à afficher
        :param sortby: le tri
        :param search: recherche à appliquer
        :param kw:
        :return:
        """
        return super().list_elements(page, sortby, search, search_in, **kw)

    def get_labels(self):
        """
        renvoit un dictionnaire avec :
        {"singulier: "",
        "pluriel": ""
        }
        :return:
        """
        return {"singulier": "équipe", "pluriel": "équipes", "page_name": "equipes"}

    def get_url_value(self):
        return "equipes"

    def get_search_criteria(self):
        return "contact"

    def get_detail_url(self):
        return "equipe"


    @http.route(
        "/cap_levage_portal/equipe/detail/<int:equipe_id>",
        auth="user",
        website=True,
    )
    def equipe_detail(self, equipe_id):
        equipe = http.request.env["res.partner"].browse(equipe_id)

        return http.request.render(
            "cap_levage_portal.equipe_detail",
            {
                "page_name": _(f"mes_{self.get_labels().get('page_name')}"),
                "equipe": equipe,
            },
        )
