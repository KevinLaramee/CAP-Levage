# -*- coding: utf-8 -*-
import base64
from datetime import datetime

from odoo import http
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.http import request
from odoo.tools.translate import _
from . import utils
from .grid_utils import TableComputeCapLevage

PPG = 2
PPR = 4


class CapLevageMateriels(http.Controller):
    @http.route(
        [
            "/cap_levage_portal/materiels",
            "/cap_levage_portal/materiels/page/<int:page>",
        ],
        auth="user",
        website=True,
    )
    @utils.check_group()
    def materiels_list(self, page=1, sortby="date", search=None, search_in="all", **kw):
        """
        Page affichant une liste de matériels.
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
                "order": "audit_suivant asc, id asc",
            },
            "equipe": {
                "label": _("Equipe"),
                "order": "equipe_id asc, agence_id asc, id asc",
            },
            "agence": {
                "label": _("Agence"),
                "order": "agence_id asc, equipe_id asc, id asc",
            },
        }
        searchbar_inputs = {
            "all": {
                "input": "all",
                "label": _("Rechercher dans tous éléments"),
            },
            "allid": {
                "input": "allid",
                "label": _("Rechercher dans tous les identifiants matériels et QRCode"),
            },
            "equipe": {
                "input": "equipe",
                "label": _("Rechercher sur toutes les équipes"),
            },
            "agence": {
                "input": "agence",
                "label": _("Rechercher sur toutes les agences"),
            },
        }

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        materiels = http.request.env["critt.equipment"]
        logged_user = request.env["res.users"].browse(request.session.uid)
        equipes_list = utils.materiels_equipe_possible_list(request, logged_user.partner_id)
        search_domain = [("equipe_id", "in", equipes_list)]
        if search is not None and search_in is not None:
            # FIXME - faire mieux ? champs store ?
            partner_ids = (
                http.request.env["res.partner"].search([("name", "ilike", search)]).ids
            )
            search_domain += [
                "|",
                "|",
                "|",
                ("num_materiel", "ilike", search),
                ("qr_code", "ilike", search),
                ("equipe_id", "in", partner_ids),
                ("agence_id", "in", partner_ids),
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
                "page_name": _("mes_materiels"),
                "default_url": "/cap_levage_portal/materiels",
                "ppr": PPR,
                "ppg": PPG,
                "bins": TableComputeCapLevage().process(all_matos, PPG, PPR),
            },
        )

    def _get_vgp_certifs_data(self, materiel):
        nb_vgp = len(materiel.rapport_controle)
        certificats = materiel.certificats
        nb_certif_creation = len(
            [certif for certif in certificats if certif.type == "creation"]
        )
        nb_certif_destruction = len(
            [certif for certif in certificats if certif.type == "reforme"]
        )
        nb_certif_controle = len(
            [certif for certif in certificats if certif.type == "controle"]
        )
        onglet_vgp_data = {
            "nb_certificats_fabrication": nb_certif_creation,
            "nb_vgp": nb_vgp,
            "nb_certificats_destruction": nb_certif_destruction,
            "nb_certificats_controle": nb_certif_controle,
        }

        sale_order_line_equipment_ids = request.env[
            "critt.sale.order.line.equipment"
        ].search([("equipment_id", "=", materiel.id)])
        sale_orders = (
            request.env["sale.order"]
                .sudo()
                .search(
                [
                    (
                        "id",
                        "in",
                        [line.order_id.id for line in sale_order_line_equipment_ids],
                    )
                ]
            )
        )

        nb_devis = len(
            [
                sale_order
                for sale_order in sale_orders
                if sale_order.state == ("sent" or "cancel")
            ]
        )
        nb_bons_commande = len(
            [
                sale_order
                for sale_order in sale_orders
                if sale_order.state == ("sale" or "done")
            ]
        )
        nb_factures = sum([sale_order.invoice_count for sale_order in sale_orders])

        onglet_devis_data = {
            "nb_devis": nb_devis,
            "nb_bons_commande": nb_bons_commande,
            "nb_factures": nb_factures,
        }
        return onglet_vgp_data, onglet_devis_data

    @http.route(
        "/cap_levage_portal/materiel/detail/<int:materiel_id>",
        auth="user",
        website=True,
    )
    @utils.check_group()
    def materiel_detail(self, materiel_id, **kw):
        """
        Affiche le détail d'un matéreil en fonction de son id
        :param materiel_id:
        :param kw:
        :return:
        """
        materiels = http.request.env["critt.equipment"]
        materiel = materiels.browse(materiel_id)
        onglet_vgp_data, onglet_devis_data = self._get_vgp_certifs_data(materiel)

        return http.request.render(
            "cap_levage_portal.materiel_detail",
            {
                "materiel": materiel,
                "onglet_vgp": onglet_vgp_data,
                "onglet_devis": onglet_devis_data,
                "page_name": _("mes_materiels"),
            },
        )

    @utils.check_group(utils.GroupWebsite.lvl_2)
    @http.route(
        "/cap_levage_portal/materiel/edit/<int:materiel_id>",
        methods=["GET"],
        auth="user",
        website=True,
    )
    def materiel_get_edit_data(self, materiel_id):
        values = self._get_materiel_edit_data(materiel_id)
        return http.request.render("cap_levage_portal.materiel_edit", values)

    def _generate_create_data(self):
        values = self._generate_edit_create_data()
        organismes_certification = http.request.env["critt.equipment.organisme"].sudo().search([], order="name asc")
        values.update({
            "page_name": _("mes_materiels"),
            "mode": "create",
            "error": {},
            "post_url": "/cap_levage_portal/materiel/create",
            "organismes_certification": organismes_certification,
        })
        return values

    @utils.check_group(utils.GroupWebsite.lvl_3)
    @http.route(
        "/cap_levage_portal/materiel/create",
        methods=["GET"],
        auth="user",
        website=True,
    )
    def materiel_get_create_data(self):
        return http.request.render("cap_levage_portal.materiel_edit", self._generate_create_data())

    def _generate_edit_create_data(self):
        logged_user = request.env["res.users"].browse(request.session.uid)
        partner = logged_user.partner_id
        company = logged_user.company_id
        equipes = (
            http.request.env["res.partner"]
                .sudo()
                .search(utils.equipe_search_domain(partner))
        )
        categories_materiel = http.request.env["critt.equipment.category"].sudo().search([], order="name asc")
        fabricants = http.request.env["critt.equipment.fabricant"].sudo().search([], order="name asc")
        # FIXME : à vérifier
        referents = http.request.env["res.partner"].sudo().search([("parent_id", "=", company.id), ("type", "=", "contact")], order="name asc")

        return {
            "categories_materiel": categories_materiel,
            "fabricants": fabricants,
            "referents": referents,
            "equipes": equipes,
        }

    def _get_materiel_edit_data(self, materiel_id):
        materiel = http.request.env["critt.equipment"].browse(materiel_id)

        onglet_vgp_data, onglet_devis_data = self._get_vgp_certifs_data(materiel)
        values = {
            "page_name": _("mes_materiels"),
            "materiel": materiel,
            "mode": "edit",
            "error": {},
            "onglet_vgp": onglet_vgp_data,
            "onglet_devis": onglet_devis_data,
            "post_url": f"/cap_levage_portal/materiel/edit/{materiel_id}"
        }
        values.update(self._generate_edit_create_data())
        return values

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.get_mandatory_fields():
            if data.get(field_name) is None:
                error[field_name] = "missing"

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

    @staticmethod
    def get_optional_fields():
        return ["image", "clear_avatar", "agence_id", "equipe_id", "last_general_observation", "is_bloque", "nombre_brins", "longueur", "cmu", "tmu",
                "model", "diametre", "grade", "num_lot", "num_commande", "referent", "upload_certificat_destruction_files",
                "upload_certificat_controle_files", "upload_certificat_fabrication_files", "date_fabrication", "an_mise_service",
                "date_dernier_audit", "organisme_id"]

    @staticmethod
    def get_mandatory_fields():
        return ["qr_code", "num_materiel", "category_id", "fabricant_id"]

    @utils.check_group(utils.GroupWebsite.lvl_2)
    @http.route(
        "/cap_levage_portal/materiel/edit/<int:materiel_id>",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def materiel_edit(self, materiel_id, **post):
        materiel = http.request.env["critt.equipment"].browse(materiel_id)
        error, error_message = self.details_form_validate(post)
        values = {}
        if not error:

            if "image" in post:
                image = post.get("image")
                if image:
                    image = image.read()
                    image = base64.b64encode(image)
                    materiel.sudo().write({"image": image})
                post.pop("image")
            if "clear_avatar" in post:
                materiel.sudo().write({"image": False})
                post.pop("clear_avatar")

            certificats = []

            certificats.extend(self._create_certificat(post, "creation", "upload_certificat_fabrication_files", 1))
            certificats.extend(self._create_certificat(post, "controle", "upload_certificat_controle_files", 2))
            certificats.extend(self._create_certificat(post, "reforme", "upload_certificat_destruction_files", 3))

            values.update({key: post[key] for key in self.get_mandatory_fields()})
            values.update(
                {key: post[key] for key in self.get_optional_fields() if key in post}
            )
            for field in {"equipe_id", "category_id", "fabricant_id", "referent"} & set(values.keys()):
                try:
                    values[field] = int(values[field])
                except:
                    values[field] = False

            values.update({"certificats": certificats})

            materiel.sudo().write(values)
            if values.get("is_bloque", False):
                materiel.action_bloquer()

            return http.request.redirect(
                f"/cap_levage_portal/materiel/detail/{materiel_id}"
            )
        else:
            values.update(self._get_materiel_edit_data(materiel_id))
            values.update(
                {
                    "error": error,
                    "error_message": error_message,
                }
            )
            return http.request.render("cap_levage_portal.materiel_edit", values)

    def _convert_empty_to_none(self, post):
        new_post = {key: (value if value != "" else None) for (key, value) in post.items()}
        return new_post

    @utils.check_group(utils.GroupWebsite.lvl_3)
    @http.route(
        "/cap_levage_portal/materiel/create",
        methods=["POST"],
        auth="user",
        website=True,
    )
    def materiel_create(self, **post):
        updated_post = self._convert_empty_to_none(post)
        error, error_message = self.details_form_validate(updated_post)
        values = {}
        if not error:

            logged_user = request.env["res.users"].browse(request.session.uid)
            if "image" in updated_post:
                image = updated_post.get("image")
                if image:
                    image = image.read()
                    image = base64.b64encode(image)
                    values.update({"image": image})
                updated_post.pop("image")

            certificats = []

            certificats.extend(self._create_certificat(updated_post, "creation", "upload_certificat_fabrication_files", 1))
            certificats.extend(self._create_certificat(updated_post, "controle", "upload_certificat_controle_files", 2))
            certificats.extend(self._create_certificat(updated_post, "reforme", "upload_certificat_destruction_files", 3))

            values.update({key: updated_post[key] for key in self.get_mandatory_fields()})
            values.update(
                {key: updated_post[key] for key in self.get_optional_fields() if key in updated_post}
            )
            for field in {"equipe_id", "category_id", "fabricant_id", "referent", "organisme_id"} & set(values.keys()):
                try:
                    values[field] = int(values[field])
                except:
                    values[field] = False

            values.update({"certificats": certificats,
                           "res_partner_id": logged_user.partner_id.id,
                           "owner_user_id": logged_user.id})

            created_materiel = http.request.env["critt.equipment"].create(values)
            if values.get("is_bloque", False):
                created_materiel.action_bloquer()

            return http.request.redirect(
                f"/cap_levage_portal/materiel/detail/{created_materiel.id}"
            )
        else:
            values.update(self._generate_create_data())
            values.update(
                {
                    "error": error,
                    "error_message": error_message,
                }
            )
            return http.request.render("cap_levage_portal.materiel_edit", values)

    def _create_certificat(self, post, type_of_certificat, input_name, sequence):
        new_files = []
        if post.get(input_name, False):
            file = post.get(input_name)
            certifcat = file.read()

            new_files.append((0, 0, {
                "desc": file.filename,
                'date': datetime.now(),
                'type': type_of_certificat,
                'fic_pdf': base64.b64encode(certifcat),
                "sequence": sequence,
            }))

        post.pop(input_name)
        return new_files


class CertifcatsList(CustomerPortal):
    def _generic_list_certificat_materiel(
            self, materiel_id, type_search, url_name, label_value, **kw
    ):
        materiel = http.request.env["critt.equipment"].browse(materiel_id)
        certificats = [
            certif for certif in materiel.certificats if certif.type == type_search
        ]
        certificats.sort(key=lambda cert: cert.date)

        values = {
            "documents": certificats,
            "materiel": materiel,
            "title": f"Certificats {label_value}",
            "emptymessage": f"Aucun certificat de {label_value} pour le matériel {materiel.num_materiel}",
            "page_name": _("mes_materiels"),
            "default_url": f"/cap_levage_portal/list/{url_name}/{materiel_id}",
        }
        return request.render("cap_levage_portal.certifs_list", values)

    @http.route(
        "/cap_levage_portal/list/certificats/controle/<int:materiel_id>",
        type="http",
        auth="user",
        website=True,
    )
    @utils.check_group(utils.GroupWebsite.lvl_2)
    def list_certificat_controle_materiel(self, materiel_id, **kw):
        return self._generic_list_certificat_materiel(
            materiel_id, "controle", "controle", "contrôle"
        )

    @http.route(
        "/cap_levage_portal/list/certificats/fabrication/<int:materiel_id>",
        type="http",
        auth="user",
        website=True,
    )
    @utils.check_group(utils.GroupWebsite.lvl_2)
    def list_certificat_creation_materiel(self, materiel_id, **kw):
        return self._generic_list_certificat_materiel(
            materiel_id, "creation", "fabrication", "fabrication"
        )

    @http.route(
        "/cap_levage_portal/list/certificats/destruction/<int:materiel_id>",
        type="http",
        auth="user",
        website=True,
    )
    @utils.check_group(utils.GroupWebsite.lvl_2)
    def list_certificat_destruction_materiel(self, materiel_id, **kw):
        return self._generic_list_certificat_materiel(
            materiel_id, "reforme", "destruction", "destruction"
        )

    @http.route(
        "/cap_levage_portal/list/vgp/<int:materiel_id>",
        type="http",
        auth="user",
        website=True,
    )
    @utils.check_group(utils.GroupWebsite.lvl_2)
    def list_certificat_creation_vgp(self, materiel_id, **kw):
        materiel = http.request.env["critt.equipment"].browse(materiel_id)
        vgps = materiel.rapport_controle
        values = {
            "documents": vgps,
            "materiel": materiel,
            "title": "VGP",
            "emptymessage": f"Aucun VGP pour le matériel {materiel.num_materiel}",
            "page_name": _("mes_materiels"),
            "default_url": f"/cap_levage_portal/list/vgp/{materiel_id}",
        }
        return request.render("cap_levage_portal.vgp_list", values)


class DevisFacturesList(CustomerPortal):
    def _generic_search(
            self,
            state_search_list,
            page_to_render,
            route_name,
            materiel_id,
            page,
            sortby,
            **kw,
    ):
        sale_order_line_equipment_ids = request.env[
            "critt.sale.order.line.equipment"
        ].search([("equipment_id", "=", materiel_id)])
        SaleOrder = request.env["sale.order"]

        domain = [
            ("id", "in", [line.order_id.id for line in sale_order_line_equipment_ids]),
            ("state", "in", state_search_list),
        ]

        searchbar_sortings = {
            "date": {"label": _("Order Date"), "order": "date_order desc"},
            "name": {"label": _("Reference"), "order": "name"},
            "stage": {"label": _("Stage"), "order": "state"},
        }

        # default sortby order
        if not sortby:
            sortby = "date"
        sort_order = searchbar_sortings[sortby]["order"]

        # count for pager
        quotation_count = SaleOrder.sudo().search_count(domain)
        # make pager
        pager = portal_pager(
            url=f"/cap_levage_portal/list/{route_name}/{materiel_id}",
            url_args={"sortby": sortby},
            total=quotation_count,
            page=page,
            step=self._items_per_page,
        )
        # search the count to display, according to the pager data
        quotations = SaleOrder.sudo().search(
            domain, order=sort_order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_quotations_history"] = quotations.ids[:100]

        values = {
            "quotations": quotations.sudo(),
            "page_name": "quote",
            "pager": pager,
            "archive_groups": [],
            "default_url": f"/cap_levage_portal/list/{route_name}/{materiel_id}",
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
        }
        return request.render(page_to_render, values)

    @utils.check_group(utils.GroupWebsite.lvl_2)
    @http.route(
        [
            "/cap_levage_portal/list/devis/<int:materiel_id>",
            "/cap_levage_portal/list/devis/<int:materiel_id>/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def list_devis_materiel(self, materiel_id, page=1, sortby=None, **kw):
        return self._generic_search(
            ["sent", "cancel"],
            "sale.portal_my_quotations",
            "devis",
            materiel_id,
            page,
            sortby,
            **kw,
        )

    @utils.check_group(utils.GroupWebsite.lvl_2)
    @http.route(
        [
            "/cap_levage_portal/list/boncommandes/<int:materiel_id>",
            "/cap_levage_portal/list/boncommandes/<int:materiel_id>/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def list_bons_commande_materiel(self, materiel_id, page=1, sortby=None, **kw):
        return self._generic_search(
            ["sale", "done"],
            "sale.portal_my_orders",
            "boncommandes",
            materiel_id,
            page,
            sortby,
            **kw,
        )

    @utils.check_group(utils.GroupWebsite.lvl_2)
    @http.route(
        [
            "/cap_levage_portal/list/factures/<int:materiel_id>",
            "/cap_levage_portal/list/factures/<int:materiel_id>/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def list_factures(self, materiel_id, page=1, sortby=None, **kw):

        sale_order_line_equipment_ids = request.env[
            "critt.sale.order.line.equipment"
        ].search([("equipment_id", "=", materiel_id)])
        sale_orders = (
            request.env["sale.order"]
                .sudo()
                .search[
                (
                    "id",
                    "in",
                    [line.order_id.id for line in sale_order_line_equipment_ids],
                )
            ]
        )
        invoices_ids = [
            invoice.id for sale in sale_orders for invoice in sale.invoice_ids
        ]

        AccountInvoice = request.env["account.move"]

        domain = [
            ("id", "in", invoices_ids),
            (
                "type",
                "in",
                (
                    "out_invoice",
                    "out_refund",
                    "in_invoice",
                    "in_refund",
                    "out_receipt",
                    "in_receipt",
                ),
            ),
        ]

        searchbar_sortings = {
            "date": {"label": _("Invoice Date"), "order": "invoice_date desc"},
            "duedate": {"label": _("Due Date"), "order": "invoice_date_due desc"},
            "name": {"label": _("Reference"), "order": "name desc"},
            "state": {"label": _("Status"), "order": "state"},
        }
        # default sort by order
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        # count for pager
        invoice_count = AccountInvoice.search_count(domain)
        # pager
        pager = portal_pager(
            url=f"/cap_levage_portal/list/factures/{materiel_id}",
            url_args={"sortby": sortby},
            total=invoice_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        invoices = AccountInvoice.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_invoices_history"] = invoices.ids[:100]

        values = {
            "invoices": invoices,
            "page_name": "invoice",
            "pager": pager,
            "archive_groups": [],
            "default_url": f"/cap_levage_portal/list/factures/{materiel_id}",
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
        }
        return request.render("account.portal_my_invoices", values)
