# -*- coding: utf-8 -*-

import time, datetime
import logging
import re
import uuid
from odoo import models, fields, api, exceptions, _
from odoo.addons.http_routing.models.ir_http import slug
from werkzeug import urls
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import odoo
import base64
import numbers

_logger = logging.getLogger(__name__)


class Questionnaire(models.Model):
    _name = "critt.certification.questionnaire"
    _description = "Questionnaire"
    _rec_name = "nom"
    _order = "nom, date_creation, id"

    # Infos Questionnaire
    nom = fields.Char(string="Nom", required=True)

    categorie = fields.Many2one("critt.equipment.category", "Catégorie", required=True)

    ids_regroupement = fields.One2many(
        "critt.certification.regroupement",
        "id_questionnaire",
        string="Regroupements",
        copy=True,
    )

    date_creation = fields.Date(
        string="Date création",
        default=datetime.datetime.today(),
        readonly=True,
        copy=False,
    )

    @api.model
    def regroupement_suivant(self, saisie_utilisateur, id_regroupement):
        questionnaire = saisie_utilisateur.id_questionnaire
        regroupements = list(enumerate(questionnaire.ids_regroupement))

        # Premier regroupement
        if id_regroupement == 0:
            return (regroupements[0][1], 0, len(regroupements) == 1)

        current_regroupement_index = regroupements.index(
            next(p for p in regroupements if p[1].id == id_regroupement)
        )

        # All the regroupements have been displayed
        if current_regroupement_index == len(regroupements) - 1:
            return (None, -1, False)
        else:
            # This will show the last regroupement
            if current_regroupement_index == len(regroupements) - 2:
                return (
                    regroupements[current_regroupement_index + 1][1],
                    current_regroupement_index + 1,
                    True,
                )
            # This will show a regular regroupement
            else:
                return (
                    regroupements[current_regroupement_index + 1][1],
                    current_regroupement_index + 1,
                    False,
                )

    # def copy(self, default=None):
    #     default = dict(default or {})
    #     Regroupement = self.env['critt.certification.regroupement']
    #     Question = self.env['critt.certification.question']
    #     newQuestionnaire = super(Questionnaire, self).copy(default)
    #
    #     for id_regroupement in self.ids_regroupement:
    #         regroupement = self.env['critt.certification.regroupement'].search([('id', '=', id_regroupement.id)])
    #
    #         vals = {'nom': regroupement.nom, 'id_questionnaire': newQuestionnaire.id}
    #         newRegroupement = Regroupement.create(vals)
    #
    #         for id_question in regroupement.ids_question:
    #             question = self.env['critt.certification.question'].search([('id', '=', id_question.id)])
    #
    #             vals = {'question': question.question, 'id_regroupement': newRegroupement.id}
    #             Question.create(vals)
    #
    #     return newQuestionnaire

    @api.model
    def create(self, vals):
        questionnaire = super(Questionnaire, self).create(vals)
        regroupement = self.env["critt.certification.regroupement"].search(
            [("id_questionnaire", "=", questionnaire.id)]
        )
        if not regroupement:
            raise ValidationError(
                _("Le questionnaire doit contenir au moins un regroupement")
            )
        return questionnaire

    def write(self, vals):
        questionnaire = super(Questionnaire, self).write(vals)
        regroupement = self.env["critt.certification.regroupement"].search(
            [("id_questionnaire", "=", self.id)]
        )
        if not regroupement:
            raise ValidationError(
                _("Le questionnaire doit contenir au moins un regroupement")
            )
        return questionnaire


class Regroupement(models.Model):
    _name = "critt.certification.regroupement"
    _description = "Regroupement"
    _rec_name = "nom"
    _order = "id"

    nom = fields.Char(string="Nom du regroupement", required=True)

    id_questionnaire = fields.Many2one(
        "critt.certification.questionnaire",
        "Questionnaire",
        ondelete="cascade",
        copy=True,
    )

    ids_question = fields.One2many(
        "critt.certification.question", "id_regroupement", string="Questions", copy=True
    )

    @api.model
    def create(self, vals):
        regroupement = super(Regroupement, self).create(vals)
        question = self.env["critt.certification.question"].search(
            [("id_regroupement", "=", regroupement.id)]
        )
        if not question:
            raise ValidationError(
                _(
                    "Le regroupement "
                    + regroupement.nom
                    + " doit contenir au moins une question"
                )
            )
        return regroupement

    def write(self, vals):
        regroupement = super(Regroupement, self).write(vals)

        for record in self:
            question = None
            question = self.env["critt.certification.question"].search(
                [("id_regroupement", "=", record.id)]
            )
            if not question:
                raise ValidationError(
                    _(
                        "Le regroupement "
                        + regroupement.nom
                        + " doit contenir au moins une question"
                    )
                )

        return regroupement


class Question(models.Model):
    _name = "critt.certification.question"
    _description = "Question"
    _rec_name = "question"
    _order = "id"

    question = fields.Char(string="Question", required=True)

    id_regroupement = fields.Many2one(
        "critt.certification.regroupement",
        "Regroupement",
        ondelete="cascade",
        required=True,
    )
    id_questionnaire = fields.Many2one(
        "critt.certification.questionnaire",
        related="id_regroupement.id_questionnaire",
        string="Questionnaire",
        ondelete="cascade",
    )

    ids_ligne_saisie_utilisateur = fields.One2many(
        "critt.certification.ligne_saisie_utilisateur", "id_question", string="Réponses"
    )

    message_erreur = fields.Char(
        string="Message d'erreur", default="Cette question est obligatoire"
    )

    #
    # def validation_question(self, post, answer_tag):
    #     self.ensure_one()
    #
    #     erreurs = {}
    #     # Réponse vide à une question obligatoire
    #     if answer_tag not in post:
    #         erreurs.update({answer_tag: self.message_erreur})
    #     if answer_tag in post and not post[answer_tag].strip():
    #         erreurs.update({answer_tag: self.message_erreur})
    #     return erreurs


class SaisieUtilisateur(models.Model):
    _name = "critt.certification.saisie_utilisateur"
    _description = "Saisie utilisateur questionnaire"
    _rec_name = "date_creation"

    id_questionnaire = fields.Many2one(
        "critt.certification.questionnaire",
        string="Questionnaire",
        required=True,
        readonly=True,
    )
    date_creation = fields.Datetime(
        "Date creation",
        default=fields.Datetime.now,
        required=True,
        readonly=True,
        copy=False,
    )

    id_client = fields.Many2one("res.partner", string="Client concerne", required=True)

    id_audit = fields.Many2one(
        "critt.certification.audit",
        string="Reponses audit",
        required=True,
        ondelete="cascade",
    )

    id_dernier_regroupement_affiche = fields.Many2one(
        "critt.certification.regroupement", string="Dernier regroupement affiché"
    )
    ids_ligne_saisie_utilisateur = fields.One2many(
        "critt.certification.ligne_saisie_utilisateur",
        "id_saisie_utilisateur",
        string="Réponses",
    )

    etat = fields.Selection(
        [
            ("nouveau", "Pas encore commencé"),
            ("passe", "Partiellement complété"),
            ("termine", "Complété"),
        ],
        string="Status",
        default="nouveau",
        readonly=True,
    )


class LigneSaisieUtilisateur(models.Model):
    _name = "critt.certification.ligne_saisie_utilisateur"
    _description = "Ligne saisie utilisateur questionnaire"
    _rec_name = "date_creation"

    id_saisie_utilisateur = fields.Many2one(
        "critt.certification.saisie_utilisateur",
        string="Saisie Utilisateur",
        required=True,
        ondelete="cascade",
    )
    id_question = fields.Many2one(
        "critt.certification.question", string="Question", required=True
    )
    id_regroupement = fields.Many2one(
        related="id_question.id_regroupement", string="Regroupement"
    )
    id_questionnaire = fields.Many2one(
        related="id_saisie_utilisateur.id_questionnaire",
        string="Questionnaire",
        store=True,
    )
    date_creation = fields.Datetime(
        "Date de création", default=fields.Datetime.now, required=True
    )

    reponse = fields.Integer(string="Réponse")

    commentaire = fields.Char(string="Commentaire")

    @api.model
    def sauv_ligne(self, id_saisie_utilisateur, question, post, answer_tag):
        vals = {
            "id_saisie_utilisateur": id_saisie_utilisateur,
            "id_question": question.id,
            "id_questionnaire": question.id_questionnaire.id,
        }
        ancienne_lsu = self.search(
            [
                ("id_saisie_utilisateur", "=", id_saisie_utilisateur),
                ("id_questionnaire", "=", question.id_questionnaire.id),
                ("id_question", "=", question.id),
            ]
        )
        ancienne_lsu.sudo().unlink()

        commentaire = answer_tag + "_com"

        if post[commentaire]:
            vals.update({"commentaire": post[commentaire]})

        if post.get(answer_tag) in ["1", "2"]:
            vals.update({"reponse": post[answer_tag]})

        self.create(vals)
        return True


# class Auditeur(models.Model):
#     _name = "critt.certification.auditeur"
#     _description = "Auditeur"
#     _rec_name = "nom"
#     _order = "nom, id"
#
#     nom = fields.Char(string = "Nom", required = True)
#
#     audits_realises = fields.One2many("critt.certification.audit", "auditeur", string = "Audits réalisés", readonly = True)


class Audit(models.Model):
    _name = "critt.certification.audit"
    _description = "Audit réalisé"
    _rec_name = "client"
    _order = "date"

    client = fields.Many2one(
        "res.partner",
        "Client",
        required=True,
        domain=[("customer", "=", "true"), ("is_company", "=", False)],
    )
    equipement = fields.Many2one(
        "critt.equipment", "Equipement", required=True, ondelete="cascade"
    )
    categorie = fields.Many2one(
        "critt.equipment.category", string="Catégorie équipement"
    )
    date = fields.Datetime(string="Date du contrôle", copy=True, required=True)
    fin = fields.Datetime(string="Fin de l'audit", copy=True, required=True)
    id_controleur = fields.Many2one("res.partner", "Contrôleur", required=False)

    questionnaire = fields.Many2one(
        "critt.certification.questionnaire", string="Questionnaire", required=True
    )
    etat_audit = fields.Selection(
        [("planifie", "Planifié"), ("debute", "Débuté"), ("termine", "Terminé")],
        string="Etat",
        default="planifie",
        readonly=True,
        copy=True,
    )

    etat_equipment_fin = fields.Char(string="Etat équipement fin audit", readonly=True)

    date_suivant = fields.Date(
        string="Date conseillée prochain audit", compute="_calcul_date_suivant"
    )
    user = fields.Many2one("res.users", string="Utilisateur")

    commande = fields.Many2one("sale.order", string="Commande")

    acces_certif = fields.Boolean(string="Accès client certificat", default=False)
    url_debuter = fields.Char(
        "Lien débuter audit", compute="_compute_url_questionnaire", copy=False
    )
    url_reponses = fields.Char(
        "Lien réponses questionnaire", compute="_compute_url_questionnaire", copy=False
    )

    etat_libelle = fields.Char("Libellé état", compute="_get_etat_libelle", copy=False)

    certif_conforme = fields.Boolean(
        string="Certificat conformite existe",
        default=False,
        invisible=True,
        readonly=True,
    )

    # Equipement à l'instant de l'audit
    e_date_pro = fields.Date(string="E date pro")  # default=equipement.audit_suivant)
    e_type = fields.Char(string="E Type")  # default=equipement.category_id.name)
    e_num = fields.Char(string="E num")  # default=equipement.num_materiel)
    e_an_mise_serv = fields.Date(
        string="E an mise serv"
    )  # default=equipement.e_an_mise_serv)
    e_fab = fields.Char(string="E fab")  # default=equipement.fabricant_id.name)
    e_coef_secu = fields.Integer(
        string="E coef secu"
    )  # default=equipement.category_id.coef_secu)
    e_cmu = fields.Char(string="E cmu")  # default=equipement.cmu)
    e_nb_brins = fields.Integer(string="E nb brins")  # default=equipement.nombre_brins)
    e_long = fields.Integer(string="E long")  # default=equipement.longueur)
    e_tmu = fields.Char(string="E tmu")  # default=equipement.tmu)
    e_model = fields.Char(string="E modèle")  # default=equipement.model)
    e_diametre = fields.Integer(string="E diamètre")  # default=equipement.diametre)
    e_grade = fields.Char(string="E grade")  # default=equipement.grade)
    e_num_lot = fields.Char(string="E Numéro de lot")  # default=equipement.num_lot)
    e_num_commande = fields.Char(
        string="E Numéro de commande"
    )  # default=equipement.num_commande)

    # Display à l'instant de l'audit
    display_cmu = fields.Boolean(string="Bool cmu")
    display_nb_brins = fields.Boolean(string="Bool nb brins")
    display_long = fields.Boolean(string="Bool long")
    display_tmu = fields.Boolean(string="Bool tmu")
    display_model = fields.Boolean(string="Bool model")
    display_diametre = fields.Boolean(string="Bool diametre")
    display_grade = fields.Boolean(string="Bool grade")
    display_num_lot = fields.Boolean(string="Bool num lot")
    display_num_commande = fields.Boolean(string="Bool num commande")

    def _get_etat_libelle(self):
        for audit in self:
            audit.etat_libelle = dict(self._fields["etat_audit"].selection).get(
                audit.etat_audit
            )

    @api.depends("equipement", "date")
    def _calcul_date_suivant(self):
        for record in self:
            if record.date and record.equipement:
                date = record.date + relativedelta(
                    months=+int(record.equipement.periode)
                )

                record.date_suivant = date
            else:
                record.date_suivant = ""

    def _compute_url_questionnaire(self):
        base_url = (
            "/"
            if self.env.context.get("relative_url")
            else self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        )
        for audit in self:
            audit.url_debuter = urls.url_join(
                base_url, "audit/completer_questionnaire/%s" % (slug(audit))
            )
            audit.url_reponses = urls.url_join(
                base_url, "audit/reponses_questionnaire/%s" % (slug(audit))
            )

    def action_reponses_questionnaire(self):
        self.ensure_one()

        client = str(self.client.id)
        queue = "/%s/0" % client
        return {
            "type": "ir.actions.act_url",
            "name": "Réponses questionnaire",
            "target": "self",
            "url": self.with_context(relative_url=True).url_reponses + queue,
        }

    def action_lancer_controle(self):
        self.ensure_one()

        self.equipement.update({"date_dernier_audit": datetime.datetime.now()})

        self.id_controleur = (
            self.env["res.users"].search([("id", "=", self.env.uid)]).partner_id.id
        )

        queue = "/%s" % self.client.id
        return {
            "type": "ir.actions.act_url",
            "name": "Démarrer questionnaire",
            "target": "self",
            "url": self.with_context(relative_url=True).url_debuter + queue,
        }

    @api.onchange("client")
    def _onchange_client(self):
        self.user = self.env["res.users"].search([("partner_id", "=", self.client.id)])
        equipements = self.env["critt.equipment"].search(
            [("owner_user_id", "=", self.user.id)]
        )
        if self.equipement not in equipements:
            self.equipement = ""
            self.categorie = ""
            self.questionnaire = ""

    @api.onchange("equipement")
    def _onchange_equipement(self):
        equipements = self.env["critt.equipment"].search(
            [("owner_user_id", "=", self.user.id)]
        )
        if self.equipement not in equipements:
            self.equipement = ""
            self.categorie = ""
            self.questionnaire = ""

        else:
            self.categorie = self.equipement.category_id.id
            questionnaire = self.env["critt.certification.questionnaire"].search(
                [("categorie", "=", self.categorie.id)]
            )
            if questionnaire:
                self.questionnaire = questionnaire.id
            else:
                self.questionnaire = ""

    @api.onchange("questionnaire")
    def _onchange_questionnaire(self):
        questionnaires = self.env["critt.certification.questionnaire"].search(
            [("categorie", "=", self.categorie.id)]
        )
        if self.questionnaire not in questionnaires:
            self.questionnaire = ""

    def copy(self, default=None):
        default = dict(default or {})
        SaisieUtilisateur = self.env["critt.certification.saisie_utilisateur"]
        LigneSaisieUtilisateur = self.env[
            "critt.certification.ligne_saisie_utilisateur"
        ]
        newAudit = super(Audit, self).copy(default)

        reponses = self.env["critt.certification.saisie_utilisateur"].search(
            [("id_audit", "=", self.id), ("id_client", "=", self.client.id)]
        )
        vals = {
            "id_questionnaire": reponses.id_questionnaire.id,
            "id_client": reponses.id_client.id,
            "id_audit": newAudit.id,
            "etat": "termine",
        }
        newSaisieUtilisateur = SaisieUtilisateur.create(vals)
        for reponse in reponses.ids_ligne_saisie_utilisateur:
            vals = {
                "id_saisie_utilisateur": newSaisieUtilisateur.id,
                "id_question": reponse.id_question.id,
                "reponse": reponse.reponse,
                "commentaire": reponse.commentaire,
            }
            LigneSaisieUtilisateur.create(vals)

        return newAudit

    @api.model
    def create(self, vals):
        audit = super(Audit, self).create(vals)

        audit.e_date_pro = audit.date_suivant
        audit.e_type = audit.equipement.category_id.name
        audit.e_num = audit.equipement.num_materiel
        audit.e_an_mise_serv = audit.equipement.an_mise_service
        audit.e_fab = audit.equipement.fabricant_id.name
        audit.e_coef_secu = audit.equipement.category_id.coef_secu
        audit.e_cmu = audit.equipement.cmu
        audit.e_nb_brins = audit.equipement.nombre_brins
        audit.e_long = audit.equipement.longueur
        audit.e_tmu = audit.equipement.tmu
        audit.e_model = audit.equipement.model
        audit.e_diametre = audit.equipement.diametre
        audit.e_grade = audit.equipement.grade
        audit.e_num_lot = audit.equipement.num_lot
        audit.e_num_commande = audit.equipement.num_commande

        audit.display_cmu = audit.equipement.display_cmu
        audit.display_nb_brins = audit.equipement.display_nombre_brins
        audit.display_long = audit.equipement.display_longueur
        audit.display_tmu = audit.equipement.display_tmu
        audit.display_model = audit.equipement.display_model
        audit.display_diametre = audit.equipement.display_diametre
        audit.display_grade = audit.equipement.display_grade
        audit.display_num_lot = audit.equipement.display_num_lot
        audit.display_num_commande = audit.equipement.display_num_commande

        return audit


# class LigneCoutAudit(models.Model):
#     _name = "critt.certification.cout_audit"
#     _description = "Audit réalisé"
#
#     categorie_equipement = fields.Many2one('critt.equipment.category', string = "Catégorie équipement", required = True)
#     cout = fields.Float(string = "Coût audit")
#
#     id_client = fields.Many2one('res.partner', string="Client")


class Certificat(models.Model):
    _name = "critt.certification.certificat"
    _description = "Stockage de certificat"
    _rec_name = "desc"
    _order = "sequence, date desc"

    desc = fields.Char(string="Description")
    date = fields.Date(string="Date")
    pdf = fields.Char(string="Certificats Cap Levage")
    fic_pdf = fields.Binary(string="Fichier pdf")
    dl_pdf = fields.Char(string="Autres Certificats")
    type = fields.Selection(
        [("creation", "Création"), ("controle", "Contrôle"), ("reforme", "Réforme")],
        string="Type",
        default="controle",
    )
    sequence = fields.Integer(string="Sequence")

    id_audit = fields.Many2one("critt.certification.audit", string="Audit")
    id_equipment = fields.Many2one("critt.equipment", string="Équipement")

    @api.model
    def create(self, vals):
        certificat = super(Certificat, self).create(vals)

        try:
            self.env.cr.execute(
                "SELECT DISTINCT id FROM ir_attachment WHERE res_model = 'critt.certification.certificat' AND res_id = %s",
                [certificat.id],
            )
            attachement_ids = [x[0] for x in self.env.cr.fetchall()]
            for attachement_id in attachement_ids:
                attachment = self.env['ir.attachment'].browse(int(attachement_id))
                access_token = attachment._generate_access_token()
                attachment.write({"access_token": access_token})
                certificat.dl_pdf = f"/web/content/{attachement_id}?download=1&access_token={access_token}"
        except:
            certificat.dl_pdf = ""

        return certificat

    @api.onchange("type")
    def _onchange_type(self):
        if self.type:
            if self.type == "creation":
                self.sequence = 1
                self.desc = "Certificat de fabrication"
                self.date = datetime.datetime.now().date()
            if self.type == "controle":
                self.sequence = 2
                self.date = datetime.datetime.now().date()
                self.desc = "Contrôle du " + self.date.strftime("%d/%m/%Y")
            if self.type == "reforme":
                self.sequence = 3
                self.desc = "Certificat de destruction"
                self.date = datetime.datetime.now().date()
        else:
            self.sequence = ""

    @api.onchange("date")
    def _onchange_date(self):
        if self.date and self.date != "" and self.type == "controle":
            self.desc = "Contrôle du " + self.date.strftime("%d/%m/%Y")


class TemplateMassCertificate(models.AbstractModel):
    _name = "report.certification.mass_certificate_template"

    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = "certification.mass_certificate_template"
        report = self.env["ir.actions.report"]._get_report_from_name(report_name)

        # Récupération des équipement nécessaires pour le rapport
        list_equipment_id = self.env[
            "critt.certification.print_mass_certificate"
        ].browse(docids)
        list_equipment_id = list_equipment_id.list_equipment.split(",")
        list_equipments = []
        for id_equipment in list_equipment_id:
            equipment = self.env["critt.equipment"].search([("id", "=", id_equipment)])
            list_equipments.append(equipment)

        # Récupération des derniers certificats de la liste d'équipements
        list_last_certif = []
        for equipment in list_equipments:
            last_certificat_equipment = self.env[
                "critt.certification.certificat"
            ].search([("id_equipment", "=", equipment.id)], order="id desc", limit=1)
            list_last_certif.append(last_certificat_equipment)

        certificats_masse = self.env[
            "critt.certification.print_mass_certificate"
        ].search([("id", "=", docids[0])])
        certificats_masse.update(
            {
                "url": "/report/pdf/certification.mass_certificate_template/%s"
                % str(certificats_masse.id),
            }
        )

        return {
            "doc_ids": docids,
            "doc_model": report.model,
            "docs": self.env[report.model].browse(docids),
            "certificats": list_last_certif,
        }


class PrintMassCertificat(models.Model):
    _name = "critt.certification.print_mass_certificate"

    list_equipment = fields.Char(string="Liste équipements certificats")
    url = fields.Char(string="URL")

    def get_selected_ids(self, context):
        selected_ids = context.get("active_ids", False)

        # Contrôle tous ont dernier certif
        for id_equipment in selected_ids:
            equipment = (
                self.env["critt.equipment"].sudo().search([("id", "=", id_equipment)])
            )
            last_certificat = (
                self.env["critt.certification.certificat"]
                .sudo()
                .search([("id_equipment", "=", equipment.id)])
            )
            if not last_certificat:
                raise ValidationError(
                    _("Un des équipements sélectionnés ne possède aucun certificat")
                )

        id_equipment_list = ",".join(map(str, selected_ids))

        certificats_masse = super(PrintMassCertificat, self).create(
            {"list_equipment": id_equipment_list}
        )

        return "/report/pdf/certification.mass_certificate_template/%s" % str(
            certificats_masse.id
        )


class TemplateRapportControle(models.AbstractModel):
    _name = "report.certification.report_controle_template"

    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = "certification.report_controle_template"
        report = self.env["ir.actions.report"]._get_report_from_name(report_name)
        cap_levage = self.env["res.partner"].sudo().search([("id", "=", 1)])

        # Récupération des équipement nécessaires pour le rapport
        list_docids = self.env["critt.certification.rapport_controle"].browse(docids)
        list_equipment_id = list_docids.list_equipment.split(",")
        list_audit_id = list_docids.list_audits.split(",")
        list_equipments = []
        list_audits = []

        list_last_audit = []
        controleurs = []
        list_lignes_saisies_utilisateurs = []
        datas = []
        client = None
        i = 0
        for id_equipment in list_equipment_id:
            equipment = self.env["critt.equipment"].search([("id", "=", id_equipment)])
            if client == None:
                client = equipment.owner_user_id.partner_id

            audit_equipement = None

            addEquipment = False
            if list_audit_id[i] != "None":
                audit_equipement = self.env["critt.certification.audit"].search(
                    [("id", "=", list_audit_id[i]), ("etat_audit", "=", "termine")],
                    order="id desc",
                    limit=1,
                )

            if audit_equipement:
                controleur = (
                    self.env["res.partner"]
                    .sudo()
                    .search([("id", "=", audit_equipement.id_controleur.id)], limit=1)
                )

                # Récupération des groupements de réponses de la liste des audits
                saisie_utilisateur = self.env[
                    "critt.certification.saisie_utilisateur"
                ].search([("id_audit", "=", audit_equipement.id)])
                if saisie_utilisateur:
                    lignes_saisies_utilisateurs = self.env[
                        "critt.certification.ligne_saisie_utilisateur"
                    ].search([("id_saisie_utilisateur", "=", saisie_utilisateur.id)])

                    if lignes_saisies_utilisateurs:
                        list_lignes_saisies_utilisateurs.append(
                            lignes_saisies_utilisateurs
                        )
                        addEquipment = True
                if addEquipment:
                    list_last_audit.append(audit_equipement)
                    list_equipments.append(equipment)
                    if controleur:
                        controleurs.append(controleur)

                        datas.append(
                            {
                                "equipment": equipment,
                                "audit": audit_equipement,
                                "controleur": controleur,
                                "reponses": lignes_saisies_utilisateurs,
                            }
                        )
            else:
                datas.append(
                    {
                        "equipment": equipment,
                        "audit": None,
                        "controleur": None,
                        "reponses": None,
                    }
                )
            i += 1

        # raise ValidationError(_(list_last_audit))

        rapport_controle = self.env["critt.certification.rapport_controle"].search(
            [("id", "=", docids[0])]
        )
        rapport_controle.update(
            {
                "number": "VGP" + str(rapport_controle.id),
                "url": "/report/pdf/certification.report_controle_template/%s"
                % str(rapport_controle.id),
                "client": client,
            }
        )

        return {
            "doc_ids": docids,
            "doc_model": report.model,
            "docs": self.env[report.model].browse(docids),
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "cap_levage": cap_levage,
            "client": client,
            "datas": datas,
        }


class RapportControle(models.Model):
    _name = "critt.certification.rapport_controle"
    _order = "create_date desc"

    number = fields.Char(string="Numéro")
    list_equipment = fields.Char(string="Liste équipements rapport")
    list_audits = fields.Char(string="Listes audits équipements")
    url = fields.Char(string="URL")
    client = fields.Many2one("res.partner", string="Client")

    def get_selected_ids(self, context):
        selected_ids = context.get("active_ids", False)

        # Contrôle tous équipements sont même client
        equipment0 = (
            self.env["critt.equipment"].sudo().search([("id", "=", selected_ids[0])])
        )
        id_client_ref = (
            self.env["res.users"]
            .sudo()
            .search([("id", "=", equipment0.owner_user_id.id)])
            .partner_id.id
        )
        for id_equipment in selected_ids:
            equipment = (
                self.env["critt.equipment"].sudo().search([("id", "=", id_equipment)])
            )
            id_client = (
                self.env["res.users"]
                .sudo()
                .search([("id", "=", equipment.owner_user_id.id)])
                .partner_id.id
            )
            if id_client_ref != id_client:
                raise ValidationError(
                    _(
                        "Les équipements d'un rapport de vgp doivent tous appartenir au même client"
                    )
                )

        id_equipment_list = ",".join(map(str, selected_ids))

        list_audits = []
        for equipment_id in selected_ids:
            last_audit_equipement = self.env["critt.certification.audit"].search(
                [("equipement", "=", equipment_id), ("etat_audit", "=", "termine")],
                order="id desc",
                limit=1,
            )
            if not last_audit_equipement:
                equipment = (
                    self.env["critt.equipment"]
                    .sudo()
                    .search([("id", "=", equipment_id)])
                )
                raise ValidationError(
                    _(
                        "Impossible de gérnérer le rapport, le matériel "
                        + equipment.num_materiel
                        + " ne possède pas d'audit."
                    )
                )
            else:
                list_audits.append(str(last_audit_equipement.id))
        list_audits = ",".join(list_audits)

        rapport_controle = super(RapportControle, self).create(
            {"list_equipment": id_equipment_list, "list_audits": list_audits}
        )

        return "/report/pdf/certification.report_controle_template/%s" % str(
            rapport_controle.id
        )
