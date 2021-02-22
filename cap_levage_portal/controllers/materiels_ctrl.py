# -*- coding: utf-8 -*-
from cap_levage_portal.controllers.grid_utils import TableComputeCapLevage
from odoo import http
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request
from odoo.tools.translate import _

PPG = 2
PPR = 5


class CapLevageWebsite(http.Controller):
    @http.route(
        [
            "/cap_levage_portal/materiels",
            "/cap_levage_portal/materiels/page/<int:page>",
        ],
        auth="public",
        website=True,
    )
    def index(self, page=1, sortby="date", search=None, search_in="allid", **kw):
        """
        Page affichange une liste de matériels.
        TODO: filtrer par equipes + gérer les filtres par état & co
        :param search_in: ou rechercher
        :param page: page à afficher
        :param sortby: le tri
        :param search: recherche à appliquer
        :param kw:
        :return:
        """
        searchbar_sortings = {
            "date": {
                "label": _("Date de prochain contrôle"),
                "order": "date_dernier_audit desc, id asc",
            }
        }
        searchbar_inputs = {
            "allid": {
                "input": "allid",
                "label": _("Rechercher dans tous les identifiants matériels"),
            },
        }

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        materiels = http.request.env["critt.equipment"]
        logged_user = request.env["res.users"].browse(request.session.uid)
        search_domain = [("owner_user_id", "=", logged_user.id)]
        if search is not None and search_in is not None:
            # TODO: chercher en plus sur ID
            search_domain += [
                "|",
                ("num_materiel", "ilike", search),
                ("qr_code", "ilike", search),
            ]
        total_items = materiels.search_count(search_domain)
        pager = portal_pager(
            url="/cap_levage_portal/materiels",
            url_args={"sortby": sortby, "search": search},
            total=total_items,
            page=page,
            step=PPG * PPR,
            scope=20,
        )
        all_matos = materiels.search(
            search_domain, order=order, limit=PPG * PPR, offset=pager["offset"]
        )
        return http.request.render(
            "cap_levage_portal.index",
            {
                "pager": pager,
                "search_in": search_in,
                "search": search,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_inputs": searchbar_inputs,
                "sortby": sortby,
                "page_name": _("Mes matériels"),
                "default_url": "/cap_levage_portal/materiels",
                "ppr": PPR,
                "ppg": PPG,
                "bins": TableComputeCapLevage().process(all_matos, PPG, PPR),
            },
        )

    @http.route(
        "/cap_levage_portal/materiel/detail/<int:materiel_id>",
        auth="public",
        website=True,
    )
    def materiel_detail(self, materiel_id, **kw):
        """
        Affiche le détail d'un matéreil en fonction de son id
        :param materiel_id:
        :param kw:
        :return:
        """
        materiels = http.request.env["critt.equipment"]
        materiel = materiels.browse(materiel_id)
        return http.request.render(
            "cap_levage_portal.materiel_detail", {"materiel": materiel}
        )
