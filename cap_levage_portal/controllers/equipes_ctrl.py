# -*- coding: utf-8 -*-
import base64

import werkzeug

from cap_levage_portal.controllers.abstract_equipes_agences_ctrl import (
    AbstractEquipesagencesCtrl,
)
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo.tools.translate import _

MANDATORY_EQUIPE_FIELDS = ["name", "title", "email"]
OPTIONAL_EQUIPE_FIELDS = ["function", "email", "phone", "mobile", "comment"]


class CapLevageEquipes(AbstractEquipesagencesCtrl, CustomerPortal):
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

    @http.route(
        "/cap_levage_portal/equipe/edit/<int:equipe_id>",
        methods=["GET"],
        auth="user",
        website=True,
    )
    def equipe_get_edit_data(self, equipe_id):
        equipe = http.request.env["res.partner"].browse(equipe_id)
        titles = http.request.env["res.partner.title"].sudo().search([])
        values = super()._prepare_home_portal_values()
        values.update(
            {
                "page_name": _(f"mes_{self.get_labels().get('page_name')}"),
                "equipe": equipe,
                "titles_list": titles,
                "edit": True,
                "error": {},
                "mode": "edit",
                "post_url": f"/cap_levage_portal/equipe/edit/{equipe_id}",
            }
        )

        return http.request.render("cap_levage_portal.equipe_edit", values)

    @http.route(
        "/cap_levage_portal/equipe/edit/<int:equipe_id>",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def equipe_edit(self, equipe_id, **post):
        equipe = http.request.env["res.partner"].browse(equipe_id)
        values = {key: post[key] for key in MANDATORY_EQUIPE_FIELDS}

        if "image_1920" in post:
            image_1920 = post.get("image_1920")
            if image_1920:
                image_1920 = image_1920.read()
                image_1920 = base64.b64encode(image_1920)
                equipe.sudo().write({"image_1920": image_1920})
            post.pop("image_1920")
        if "clear_avatar" in post:
            equipe.sudo().write({"image_1920": False})
            post.pop("clear_avatar")

        values.update({key: post[key] for key in OPTIONAL_EQUIPE_FIELDS if key in post})

        equipe.sudo().write(values)
        return werkzeug.utils.redirect(f"/cap_levage_portal/equipe/detail/{equipe_id}")

    @http.route(
        "/cap_levage_portal/equipe/archive/<int:equipe_id>",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def equipe_delete(self, equipe_id):
        equipe = http.request.env["res.partner"].browse(equipe_id)
        values = {"active": False}
        equipe.sudo().write(values)
        return werkzeug.utils.redirect("/cap_levage_portal/equipes")

    @http.route(
        "/cap_levage_portal/equipe/create",
        methods=["GET"],
        auth="user",
        website=True,
    )
    def equipe_get_create_data(self):
        titles = http.request.env["res.partner.title"].sudo().search([])
        values = super()._prepare_home_portal_values()
        values.update(
            {
                "page_name": _(f"mes_{self.get_labels().get('page_name')}"),
                "titles_list": titles,
                "edit": True,
                "error": {},
                "mode": "create",
                "post_url": "/cap_levage_portal/equipe/create",
            }
        )

        return http.request.render("cap_levage_portal.equipe_edit", values)

    @http.route(
        "/cap_levage_portal/equipe/create",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def equipe_get_create(self, **post):
        logged_user = http.request.env["res.users"].browse(http.request.session.uid)
        values = {key: post[key] for key in MANDATORY_EQUIPE_FIELDS}
        values.update({key: post[key] for key in OPTIONAL_EQUIPE_FIELDS if key in post})
        values.update({"type": "contact", "parent_id": logged_user.partner_id.id})
        new_equipe = http.request.env["res.partner"].create(values)

        if "image_1920" in post:
            image_1920 = post.get("image_1920")
            if image_1920:
                image_1920 = image_1920.read()
                image_1920 = base64.b64encode(image_1920)
                new_equipe.sudo().write({"image_1920": image_1920})

        return werkzeug.utils.redirect(
            f"/cap_levage_portal/equipe/detail/{new_equipe.id}"
        )
