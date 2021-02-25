# -*- coding: utf-8 -*-
import werkzeug

from cap_levage_portal.controllers.abstract_equipes_agences_ctrl import (
    AbstractEquipesagencesCtrl
)
from odoo import http

from odoo.tools.translate import _

MANDATORY_EQUIPE_FIELDS = ["name", "title", "email"]
OPTIONAL_EQUIPE_FIELDS = ["function", "phone", "mobile", "comment", "image_1920"]


class CapLevageEquipes(AbstractEquipesagencesCtrl, http.Controller):
    def __init__(self):
        super(CapLevageEquipes, self).__init__()

    @http.route(
        [
            "/cap_levage_portal/equipes",
            "/cap_levage_portal/equipes/page/<int:page>",
        ],
        auth="user",
        website=True,
    )
    def list_equipes(self, page=1, sortby="name", search=None, search_in="allid", **kw):
        """
        Page affichange une liste de matériels.
        :param search_in: ou rechercher
        :param page: page à afficher
        :param sortby: le tri
        :param search: recherche à appliquer
        :param kw:
        :return:
        """
        return super(CapLevageEquipes, self).list_elements(page, sortby, search, search_in, **kw)

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

    def is_agence(self):
        return False

    def is_equipe(self):
        return True

    def get_optional_fields(self):
        return OPTIONAL_EQUIPE_FIELDS

    def get_mandatory_fields(self):
        return MANDATORY_EQUIPE_FIELDS

    @http.route(
        "/cap_levage_portal/equipe/detail/<int:equipe_id>",
        auth="user",
        website=True,
    )
    def equipe_detail(self, equipe_id):
        equipe = http.request.env["res.partner"].browse(equipe_id)

        values = self._compute_generic_values()
        values.update(
            {
                "page_name": _(f"mes_{self.get_labels().get('page_name')}"),
                "partner": equipe,
            })
        return http.request.render(
            "cap_levage_portal.equipe_detail", values
        )

    @http.route(
        "/cap_levage_portal/equipe/edit/<int:equipe_id>",
        methods=["GET"],
        auth="user",
        website=True,
    )
    def equipe_get_edit_data(self, equipe_id):
        values = self.partner_get_edit_data(equipe_id)
        return http.request.render("cap_levage_portal.equipe_edit", values)

    @http.route(
        "/cap_levage_portal/equipe/edit/<int:equipe_id>",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def equipe_edit(self, equipe_id, **post):
        return self.update_res_partner(equipe_id, post, "cap_levage_portal.equipe_edit")

    @http.route(
        "/cap_levage_portal/equipe/archive/<int:equipe_id>",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def equipe_delete(self, equipe_id):
        return self.archive_res_partner(equipe_id)

    @http.route(
        "/cap_levage_portal/equipe/create",
        methods=["GET"],
        auth="user",
        website=True,
    )
    def equipe_get_create_data(self):
        values = self.partner_get_create_data()
        return http.request.render("cap_levage_portal.equipe_edit", values)

    @http.route(
        "/cap_levage_portal/equipe/create",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def equipe_get_create(self, **post):
        return self.partner_create(post, "cap_levage_portal.equipe_edit")
