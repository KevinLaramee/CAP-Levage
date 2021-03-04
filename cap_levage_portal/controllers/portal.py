# -*- coding: utf-8 -*-
from . import utils
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class CustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self):
        values = super(CustomerPortal, self)._prepare_home_portal_values()
        logged_user = request.env["res.users"].browse(request.session.uid)
        partner = logged_user.partner_id
        values["nb_materiels_count"] = request.env["critt.equipment"].search_count(
            [
                "|",
                ("referent", "=", logged_user.partner_id.id),
                ("referent", "child_of", logged_user.partner_id.id),
            ]
        )
        values["nb_equipes_count"] = request.env["res.partner"].search_count(
            utils.equipe_search_domain(partner)
        )
        values["nb_agences_count"] = request.env["res.partner"].search_count(
            utils.agence_search_domain(partner)
        )
        return values
