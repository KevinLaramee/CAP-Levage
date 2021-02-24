# -*- coding: utf-8 -*-
from cap_levage_portal.controllers.abstract_equipes_agences_ctrl import (
    AbstractEquipesagencesCtrl,
)
from odoo import http

from odoo.tools.translate import _

class CapLevageEquipes(AbstractEquipesagencesCtrl, http.Controller):
    @http.route(
        [
            "/cap_levage_portal/agences",
            "/cap_levage_portal/agences/page/<int:page>",
        ],
        auth="public",
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
        return {"singulier": "agence", "pluriel": "agences", "page_name": "agences"}

    def get_url_value(self):
        return "agences"

    def get_search_criteria(self):
        return "delivery"

    def get_detail_url(self):
        return "agence"

    @http.route(
        "/cap_levage_portal/agence/detail/<int:agence_id>",
        auth="user",
        website=True,
    )
    def agence_detail(self, agence_id):
        agence = http.request.env["res.partner"].browse(agence_id)

        return http.request.render(
            "cap_levage_portal.agence_detail",
            {
                "page_name": _(f"mes_{self.get_labels().get('page_name')}"),
                "agence": agence,
            },
        )
