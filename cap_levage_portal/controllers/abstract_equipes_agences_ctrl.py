# -*- coding: utf-8 -*-
from abc import abstractmethod

from cap_levage_portal.controllers.grid_utils import TableComputeCapLevage
from odoo import http
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

    @abstractmethod
    def get_url_value(self):
        pass

    @abstractmethod
    def get_detail_url(self):
        pass

    @abstractmethod
    def get_search_criteria(self):
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
                "label": _(f"Nombre d'{labels.get('singulier')}"),
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
        search_domain = [
            ("parent_id", "=", logged_user.partner_id.id),
            ("type", "=", self.get_search_criteria()),
        ]
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
        return http.request.render(
            "cap_levage_portal.equipes_list",
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
                "ppr": PPR,
                "ppg": PPG,
                "bins": TableComputeCapLevage().process(all_equipes, PPG, PPR),
            },
        )
