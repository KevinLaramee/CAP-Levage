# -*- coding: utf-8 -*-

from cap_levage_portal.controllers.abstract_equipes_agences_ctrl import (
    AbstractEquipesagencesCtrl,
)
from odoo import http

from odoo.tools.translate import _

MANDATORY_AGENCE_FIELDS = ["name", "street", "country_id", "city", "zip"]
OPTIONAL_AGENCE_FIELDS = ["email", "phone", "mobile", "comment"]


class CapLevageAgences(AbstractEquipesagencesCtrl, http.Controller):
    def __init__(self):
        super(CapLevageAgences, self).__init__()

    @http.route(
        [
            "/cap_levage_portal/agences",
            "/cap_levage_portal/agences/page/<int:page>",
        ],
        auth="user",
        website=True,
    )
    def list_agences(self, page=1, sortby="name", search=None, search_in="allid", **kw):
        """
        Page affichange une liste de matériels.
        :param search_in: ou rechercher
        :param page: page à afficher
        :param sortby: le tri
        :param search: recherche à appliquer
        :param kw:
        :return:
        """
        return super(CapLevageAgences, self).list_elements(page, sortby, search, search_in, **kw)

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

    def is_agence(self):
        return True

    def is_equipe(self):
        return False

    @http.route(
        "/cap_levage_portal/agence/detail/<int:agence_id>",
        auth="user",
        website=True,
    )
    def agence_detail(self, agence_id):
        agence = http.request.env["res.partner"].browse(agence_id)

        values = self._compute_generic_values()
        values.update({
            "page_name": _(f"mes_{self.get_labels().get('page_name')}"),
            "partner": agence,
        })
        return http.request.render(
            "cap_levage_portal.agence_detail",
            values,
        )

    @http.route(
        "/cap_levage_portal/agence/edit/<int:agence_id>",
        methods=["GET"],
        auth="user",
        website=True,
    )
    def agence_get_edit_data(self, agence_id):
        values = self.partner_get_edit_data(agence_id)
        return http.request.render("cap_levage_portal.agence_edit", values)

    @http.route(
        "/cap_levage_portal/agence/edit/<int:agence_id>",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def agence_edit(self, agence_id, **post):
        return self.update_res_partner(agence_id, post, MANDATORY_AGENCE_FIELDS, OPTIONAL_AGENCE_FIELDS)

    @http.route(
        "/cap_levage_portal/agence/archive/<int:agence_id>",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def agence_delete(self, agence_id):
        return self.archive_res_partner(agence_id)

    @http.route(
        "/cap_levage_portal/agence/create",
        methods=["GET"],
        auth="user",
        website=True,
    )
    def agence_get_create_data(self):
        values = self.partner_get_create_data()
        return http.request.render("cap_levage_portal.agence_edit", values)

    @http.route(
        "/cap_levage_portal/agence/create",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def agence_get_create(self, **post):
        return self.partner_create(post, MANDATORY_AGENCE_FIELDS, OPTIONAL_AGENCE_FIELDS)

