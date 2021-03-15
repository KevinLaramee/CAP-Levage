# -*- coding: utf-8 -*-
import base64
from abc import abstractmethod

from .grid_utils import TableComputeCapLevage
from . import utils
from odoo import http, tools
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request
from odoo.tools.translate import _

PPG = 2
PPR = 5


class AbstractEquipesagencesCtrl:
    @abstractmethod
    def get_labels(self):
        """
        renvoit un dictionnaire avec :
        {"singulier: "",
        "pluriel": ""
        }
        :return:
        """
        pass

    def _compute_generic_values(self):
        return {
            "is_agence": self.is_agence(),
            "is_equipe": self.is_equipe(),
            "error": {},
        }

    @abstractmethod
    def get_url_value(self):
        pass

    @abstractmethod
    def is_agence(self):
        pass

    @abstractmethod
    def is_equipe(self):
        pass

    @abstractmethod
    def get_detail_url(self):
        pass

    @abstractmethod
    def get_search_criteria(self):
        pass

    @abstractmethod
    def get_optional_fields(self):
        pass

    @abstractmethod
    def get_mandatory_fields(self):
        pass

    def list_elements(self, page, sortby, search, search_in, **kw):
        """
        Page affichant une liste de matériels.
        TODO: filtrer par equipes + gérer les filtres par état & co
        :param search_in: ou rechercher
        :param page: page à afficher
        :param sortby: le tri
        :param search: recherche à appliquer
        :param kw:
        :return:
        """
        labels = self.get_labels()
        searchbar_sortings = {
            "name": {
                "label": _(f"Nom de l'{labels.get('singulier')}"),
                "order": "name desc, id asc",
            },
            "nbequipment": {
                "label": _("Nombre de matériel"),
                "order": "ids_equipements desc, id asc",
            },
        }
        searchbar_inputs = {
            "both": {
                "input": "both",
                "label": _("Rechercher par nom ou email"),
            },
            "name": {
                "input": "name",
                "label": _("Rechercher par nom"),
            },
            "email": {
                "input": "email",
                "label": _("Rechercher par email"),
            },
        }

        # default sort by value
        if not sortby:
            sortby = "name"
        order = searchbar_sortings[sortby]["order"]

        equipes = http.request.env["res.partner"]
        logged_user = request.env["res.users"].browse(request.session.uid)
        search_domain = utils.partner_search_domain(logged_user.partner_id, self.get_search_criteria())
        if search is not None and search_in is not None:
            if search_in == "both":
                search_domain += [
                    "|",
                    ("name", "ilike", search),
                    ("email", "ilike", search),
                ]
            if search_in == "name":
                search_domain += [("name", "ilike", search)]
            if search_in == "email":
                search_domain += [("email", "ilike", search)]
        total_items = equipes.search_count(search_domain)
        pager = portal_pager(
            url=f"/cap_levage_portal/{self.get_url_value()}",
            url_args={"sortby": sortby, "search": search},
            total=total_items,
            page=page,
            step=PPG * PPR,
            scope=20,
        )
        all_equipes = equipes.search(
            search_domain, order=order, limit=PPG * PPR, offset=pager["offset"]
        )
        [equipe._count_equipments() for equipe in all_equipes]
        values = self._compute_generic_values()
        values.update(
            {
                "pager": pager,
                "detail_url": f"{self.get_detail_url()}",
                "search_in": search_in,
                "search": search,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_inputs": searchbar_inputs,
                "sortby": sortby,
                "page_name": _(f"mes_{labels.get('page_name')}"),
                "default_url": f"/cap_levage_portal/{self.get_url_value()}",
                "create_url": f"/cap_levage_portal/{self.get_detail_url()}/create",
                "ppr": PPR,
                "ppg": PPG,
                "bins": TableComputeCapLevage().process(all_equipes, PPG, PPR),
            }
        )

        return http.request.render(
            "cap_levage_portal.equipes_list",
            values,
        )

    def update_res_partner(self, partner_id, post, error_page):
        updated_post = utils.convert_empty_to_none(post)
        partner = http.request.env["res.partner"].browse(partner_id)
        error, error_message = self.details_form_validate(updated_post)
        values = {}
        if not error:
            values.update({key: updated_post[key] for key in self.get_mandatory_fields()})

            if "image_1920" in updated_post:
                image_1920 = updated_post.get("image_1920")
                if image_1920:
                    image_1920 = image_1920.read()
                    image_1920 = base64.b64encode(image_1920)
                    partner.sudo().write({"image_1920": image_1920})
                updated_post.pop("image_1920")
            if "clear_avatar" in updated_post:
                partner.sudo().write({"image_1920": False})
                updated_post.pop("clear_avatar")

            values.update(
                {key: updated_post[key] for key in self.get_optional_fields() if key in updated_post}
            )
            for field in {"country_id", "state_id"} & set(values.keys()):
                try:
                    values[field] = int(values[field])
                except:
                    values[field] = False
            partner.sudo().write(values)
            return http.request.redirect(
                f"/cap_levage_portal/{self.get_detail_url()}/detail/{partner_id}"
            )
        else:
            values.update(self._compute_generic_values())
            values.update(self.partner_get_edit_data(partner_id))
            values.update(
                {
                    "error": error,
                    "error_message": error_message,
                }
            )
            return http.request.render(error_page, values)

    def archive_res_partner(self, partner_id):
        agence = http.request.env["res.partner"].browse(partner_id)
        values = {"active": False}
        agence.sudo().write(values)
        return http.request.redirect(f"/cap_levage_portal/{self.get_url_value()}")

    def partner_get_create_data(self):
        titles = http.request.env["res.partner.title"].sudo().search([])
        countries = request.env["res.country"].sudo().search([])
        values = self._compute_generic_values()
        values.update(
            {
                "page_name": _(f"mes_{self.get_labels().get('page_name')}"),
                "titles_list": titles,
                "countries": countries,
                "edit": True,
                "error": {},
                "mode": "create",
                "post_url": f"/cap_levage_portal/{self.get_detail_url()}/create",
            }
        )
        return values

    def partner_get_edit_data(self, partner_id):
        partner = http.request.env["res.partner"].browse(partner_id)
        titles = http.request.env["res.partner.title"].sudo().search([])
        countries = request.env["res.country"].sudo().search([])
        values = self._compute_generic_values()
        values.update(
            {
                "page_name": _(f"mes_{self.get_labels().get('page_name')}"),
                "partner": partner,
                "titles_list": titles,
                "countries": countries,
                "edit": True,
                "mode": "edit",
                "post_url": f"/cap_levage_portal/{self.get_detail_url()}/edit/{partner_id}",
            }
        )
        return values

    def partner_create(self, post, error_page):
        updated_post = utils.convert_empty_to_none(post)
        logged_user = http.request.env["res.users"].browse(http.request.session.uid)
        error, error_message = self.details_form_validate(updated_post)
        values = {}
        if not error:
            values.update({key: updated_post[key] for key in self.get_mandatory_fields()})
            values.update(
                {key: updated_post[key] for key in self.get_optional_fields() if key in updated_post}
            )
            values.update(
                {
                    "type": self.get_search_criteria(),
                    "parent_id": logged_user.partner_id.id,
                }
            )
            new_partner = http.request.env["res.partner"].create(values)

            if "image_1920" in updated_post:
                image_1920 = updated_post.get("image_1920")
                if image_1920:
                    image_1920 = image_1920.read()
                    image_1920 = base64.b64encode(image_1920)
                    new_partner.sudo().write({"image_1920": image_1920})

            return http.request.redirect(
                f"/cap_levage_portal/{self.get_detail_url()}/detail/{new_partner.id}"
            )
        else:
            values.update(self._compute_generic_values())
            values.update(self.partner_get_create_data())
            values.update(
                {
                    "error": error,
                    "error_message": error_message,
                }
            )
            return http.request.render(error_page, values)

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.get_mandatory_fields():
            if not data.get(field_name):
                error[field_name] = "missing"

        # email validation
        if data.get("email") and not tools.single_email_re.match(data.get("email")):
            error["email"] = "error"
            error_message.append(
                _("Invalid Email! Please enter a valid email address.")
            )

        # error message for empty required fields
        if [err for err in error.values() if err == "missing"]:
            error_message.append(_("Some required fields are empty."))

        unknown = [
            k
            for k in data
            if k not in self.get_mandatory_fields() + self.get_optional_fields()
        ]
        if unknown:
            error["common"] = "Unknown field"
            error_message.append("Unknown field '%s'" % ",".join(unknown))

        return error, error_message
