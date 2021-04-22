import datetime
import logging
from datetime import datetime

from PIL import Image
from dateutil.relativedelta import relativedelta

from odoo import api, models, fields, tools, _
from odoo.exceptions import ValidationError


class MaintenanceEquipment(models.Model):
    _name = "critt.equipment"
    _inherit = "mail.thread"
    _description = "Equipment"
    _order = "owner_user_id"
    _rec_name = "num_materiel"
    logger = logging.getLogger(__name__)

    name = fields.Char("Nom", translate=True)
    active = fields.Boolean(default=True)

    owner_user_id = fields.Many2one("res.users", string="Client", required=True)
    res_partner_id = fields.Many2one(
        "res.partner",
        string="Client",
        required=True,
        domain="[('has_account', '=', True)]",
        track_visibility=True,
    )
    num_materiel = fields.Char(
        string="Numéro gravé", required=True, copy=False, track_visibility=True
    )
    color = fields.Integer("Color Index")
    an_mise_service = fields.Date(string="Date de mise en service")
    scrap_date = fields.Date(string="Année de réforme")
    partner_create = fields.Many2one("res.partner", string="Responsable création")
    partner_destruct = fields.Many2one("res.partner", string="Responsable destruction")

    referent = fields.Many2one(
        "res.partner",
        string="Référent",
        domain="[('parent_id', '=', res_partner_id)]",
        track_visibility=True,
    )

    referent2 = fields.Many2one(
        "res.partner", string="Référent", compute="_get_referent"
    )

    # num_client = fields.Char(string='Numéro interne (client)')

    in_or_out = fields.Selection(
        [("in", "Entrée"), ("out", "Sortie")],
        string="Entrée ou sortie",
        default="",
        readonly=True,
    )
    date_entree = fields.Datetime(
        string="Date d'entrée", readonly=True, track_visibility=True
    )
    date_sortie = fields.Datetime(
        string="Date sortie", readonly=True, track_visibility=True
    )

    date_fabrication = fields.Date(string="Date de Fabrication", track_visibility=True)

    certif_creation = fields.Boolean(
        string="Certificat creation existe",
        default=False,
        invisible=True,
        readonly=True,
    )
    certif_destruction = fields.Boolean(
        string="Certificat destruction existe",
        default=False,
        invisible=True,
        readonly=True,
    )

    derniere_facture = fields.Many2one("account.move", string="Dernière facture")
    num_derniere_facture = fields.Char(string="Numéro dernière facture")

    internal_no = fields.Char("Numéro interne", copy=False)
    periode = fields.Integer(
        string="Periodicité des audits (en mois)", required=True, default=0
    )

    is_bloque = fields.Boolean(string="Matériel bloqué", default=False, track_visibility=True)
    date_bloque = fields.Date(string="Bloqué le")

    statuts = [
        ("ok", "UTILISABLE"),
        ("en_cours", "À RÉPARER"),
        ("bloque", "INTERDIT D'EMPLOI"),
        ("reforme", "RÉFORMÉ"),
        ("detruit", "DÉTRUIT"),
    ]

    statut = fields.Selection(statuts, string="Etat", default="ok", readonly=True)

    orga_certif = fields.Char(string="Organisme certifiant", default="Cap Levage")

    of_cap_levage = fields.Boolean(string="Géré par Cap Levage", default=False)
    from_cap_levage = fields.Boolean(string="Créé par Cap Levage", default=True)
    is_new = fields.Boolean(string="Est neuf", default=True)

    qr_code = fields.Char(
        string="Identifiant QR Code", copy=False, track_visibility=True
    )

    sale_order_count = fields.Integer(
        string="Compteur devis", compute="_count_sale_order"
    )

    sale_order_count_for_portal = fields.Integer(
        string="Compteur devis", compute="_count_sale_order_for_portal"
    )

    quote_in_progress = fields.Integer(
        string="Compteur devis", compute="_count_sale_order"
    )
    localisation_description = fields.Char(string="Attribution")
    fabricant_id = fields.Many2one("critt.equipment.fabricant", string="Fabricant")
    agence_id = fields.Many2one(
        "res.partner",
        related="equipe_id.parent_id",
        string="Agence / secteur",
        track_visibility=True,
    )
    equipe_id = fields.Many2one(
        "res.partner",
        string="Équipe",
        domain="[('type', '=', 'contact')]",
        track_visibility=True,
    )

    horodating_ids = fields.One2many(
        "critt.horodating", "equipment_id", string="Ids Horodatage"
    )

    cmu = fields.Char(string="CMU (tonnes)")
    nombre_brins = fields.Integer(string="Nombre de brins")
    longueur = fields.Float(string="Longueur (ml)")
    tmu = fields.Char(string="TMU (daN)")
    model = fields.Char(string="Modèle matériel")
    diametre = fields.Float(string="Diamètre (mm)")
    grade = fields.Char(string="Grade")
    num_lot = fields.Char(string="Numéro de lot")
    num_commande = fields.Char(string="Numéro de commande")

    display_nombre_brins = fields.Boolean(
        string="Afficher le champ nombre brins", default=False
    )
    display_longueur = fields.Boolean(
        string="Afficher le champ longueur", default=False
    )
    display_cmu = fields.Boolean(string="Afficher le champ CMU", default=False)
    display_tmu = fields.Boolean(string="Afficher le champ TMU", default=False)
    display_model = fields.Boolean(string="Afficher le champ modèle", default=False)
    display_diametre = fields.Boolean(
        string="Afficher le champ diamètre", default=False
    )
    display_grade = fields.Boolean(string="Afficher le champ grade", default=False)
    display_num_lot = fields.Boolean(
        string="Afficher le champ numéro de lot", default=False
    )
    display_num_commande = fields.Boolean(
        string="Afficher le champ numéro de commande", default=False
    )

    montage_special = fields.Boolean(string="Montage spécial", default=False)

    last_general_observation = fields.Char(string="Dernière observation générale")

    observ_blocage = fields.Char(string="Observation après blocage client")

    # category_id = fields.Many2one(string="Catégorie")
    category_id = fields.Many2one(
        "critt.equipment.category", string="Type", required=True, track_visibility=True
    )
    # is_elingue = fields.Boolean(string="Est une élingue")

    organisme_id = fields.Many2one(
        "critt.equipment.organisme",
        required=True,
        string="Organisme de certification",
        track_visibility=True,
    )

    datetime_destruction = fields.Datetime(string="Date destruction")

    audits = fields.One2many(
        "critt.certification.audit", "equipement", string="Audits", readonly=True
    )
    date_dernier_audit = fields.Datetime(
        string="Date dernier audit", track_visibility=True, copy=False
    )
    audit_suivant = fields.Date(string="Date prochain contrôle", readonly=True)
    audit_suivant_color = fields.Char(
        "audit_suivant_color", compute="_get_audit_suivant_color", copy=False
    )
    audit_suivant_color_index = fields.Integer(
        compute="_get_audit_suivant_color_index", copy=False
    )

    date_last_audit = fields.Char(
        "Date dernier audit", compute="_get_date_last_audit", copy=False
    )
    last_audit = fields.Integer("Dernier audit", compute="_get_last_audit", copy=False)
    date_last_audit_string = fields.Char(
        "date_last_audit_string", compute="_get_date_last_audit_string", copy=False
    )

    last_certificat = fields.Char(
        "Dernier audit", compute="_get_last_certificat", copy=False
    )

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Image(
        "Photo",
        max_width=1024,
        max_height=1024,
        attachment=True,
        help="This field holds the image used as image for the product, limited to 1024x1024px.",
    )
    image_medium = fields.Image(
        "Image 128", related="image", max_width=128, max_height=128, store=True
    )
    image_small = fields.Image(
        "Image 64", related="image", max_width=64, max_height=64, store=True
    )

    # is_ok = fields.Boolean("", compute="_get_is_ok", copy=False)

    statut_libelle = fields.Char(
        "Libellé statut", compute="_get_statut_libelle", copy=False
    )
    statut_index = fields.Integer(
        "Index statut", compute="_get_statut_index", copy=False
    )

    image_photo = fields.Char("image_photo", compute="_get_image_photo", copy=False)
    image_photo2 = fields.Char("image_photo2", compute="_get_image_photo2", copy=False)
    image_photo_mime_type = fields.Char(
        "image_photo_mime_type", compute="_get_image_photo_mime_type", copy=False
    )
    image_photo_exist = fields.Boolean(
        "image_photo_exist", compute="_get_image_photo_exist", default=False, copy=False
    )

    audit_depasse = fields.Boolean("Date audit depasse", compute="_is_audit_depasse")

    certificats = fields.One2many(
        "critt.certification.certificat", "id_equipment", string="Certificats"
    )

    orderLineEquipment = fields.One2many(
        "critt.sale.order.line.equipment", "equipment_id"
    )

    work_done_on_equipment = fields.One2many(
        "critt.sale.order.line.equipment", compute="_work_done_on_equipment"
    )

    switch = fields.Char(string="Champ save photo", default="1")

    is_duplicated = fields.Boolean(string="Est Duplicata", default=False)

    rapport_controle = fields.One2many(
        "critt.certification.rapport_controle", compute="_compute_rapport_controle"
    )

    def action_valider(self):
        self.statut = "ok"
        self.is_bloque = False
        self.date_bloque = None

    def action_bloquer(self):
        self.statut = "bloque"
        self.is_bloque = True
        self.date_bloque = fields.date.today()

        Horodating = self.env["critt.horodating"]

        vals = {
            "user": self.env.user.id,
            "action": "Blocage matériel",
            "equipment_id": self.id,
        }

        Horodating.create(vals)

    def generate_mass_certificate_controle(self, context):
        selected_ids = context.get("active_ids", False)
        Audit = self.env["critt.certification.audit"]
        SaisieUtilisateur = self.env["critt.certification.saisie_utilisateur"]
        LigneSaisieUtilisateur = self.env[
            "critt.certification.ligne_saisie_utilisateur"
        ]
        Certificat = self.env["critt.certification.certificat"]

        for id_equipment in selected_ids:
            equipment = self.env["critt.equipment"].search([("id", "=", id_equipment)])
            client = equipment.owner_user_id.partner_id.id
            date = datetime.now()  # .strftime("%d/%m/%Y %H:%M")
            fin = datetime.now() + relativedelta(
                hours=+1
            )  # .strftime("%d/%m/%Y %H:%M")
            controleur = (
                self.env["res.users"].search([("id", "=", self.env.uid)]).partner_id.id
            )

            questionnaire = self.env["critt.certification.questionnaire"].search(
                [("categorie", "=", equipment.category_id.id)],
                limit=1,
                order="date_creation desc",
            )
            if not questionnaire:
                raise ValidationError(
                    _(
                        "Il n'existe pas de questionnaire pour contrôler ce type de matériel"
                    )
                )
            else:
                vals = {
                    "client": client,
                    "equipement": equipment.id,
                    "questionnaire": questionnaire.id,
                    "date": date,
                    "fin": fin,
                    "id_controleur": controleur,
                    "categorie": equipment.category_id.id,
                    "etat_audit": "termine",
                    "acces_certif": True,
                    "certif_conforme": True,
                }

                audit = Audit.create(vals)

                equipment.update({"date_dernier_audit": datetime.now()})

            regroupements = self.env["critt.certification.regroupement"].search(
                [("id_questionnaire", "=", questionnaire.id)]
            )
            vals_saisie = {
                "id_questionnaire": questionnaire.id,
                "id_client": client,
                "id_audit": audit.id,
                "etat": "termine",
            }
            saisie_utilisateur = SaisieUtilisateur.create(vals_saisie)
            for regroupement in regroupements:
                questions = self.env["critt.certification.question"].search(
                    [("id_regroupement", "=", regroupement.id)]
                )

                for question in questions:
                    vals_ligne_saisie = {
                        "id_saisie_utilisateur": saisie_utilisateur.id,
                        "id_question": question.id,
                        "id_regroupement": regroupement.id,
                        "id_questionnaire": questionnaire.id,
                        "reponse": 1,
                    }
                    ligne_saisie_utilisateur = LigneSaisieUtilisateur.create(
                        vals_ligne_saisie
                    )

            equipment.update({"statut": "ok", "audit_suivant": audit.date_suivant})
            audit.update({"etat_equipment_fin": "Certifié"})
            # Création lien certif vue equipements
            # Remplissage du champ pdf
            pdf = "/report/pdf/certification.report_certificat_conforme/" + str(
                audit.id
            )

            # Remplissage du champ desc
            desc = "Contrôle du " + audit.date.strftime("%d/%m/%Y")

            vals_certif = {
                "desc": desc,
                "date": audit.date,
                "pdf": pdf,
                "id_audit": audit.id,
                "id_equipment": audit.equipement.id,
                "type": "controle",
                "sequence": 2,
            }

            Certificat.create(vals_certif)
            audit.update({"certif_conforme": True})

    def entree_masse(self, context):
        selected_ids = context.get("active_ids", False)

        for equipment_id in selected_ids:
            equipment = self.env["critt.equipment"].search([("id", "=", equipment_id)])
            if equipment.in_or_out == "in":
                raise ValidationError(
                    _("L'un des matériels séléctionnés est déjà entré")
                )
            else:
                equipment.date_entree = datetime.now()
                equipment.in_or_out = "in"

    def sortie_masse(self, context):
        selected_ids = context.get("active_ids", False)

        for equipment_id in selected_ids:
            equipment = self.env["critt.equipment"].search([("id", "=", equipment_id)])
            if equipment.in_or_out == "out":
                raise ValidationError(
                    _("L'un des matériels séléctionnés est déjà sortit")
                )
            else:
                equipment.date_sortie = datetime.now()
                equipment.in_or_out = "out"

    def maj_rapport_vgp(self):
        list_rapport_vgp_vides = self.env[
            "critt.certification.rapport_controle"
        ].search(["|", ("list_audits", "=", ""), ("list_audits", "=", None)])

        for rapport_vgp in list_rapport_vgp_vides:
            list_audits_rapport = []

            list_ids_equipments_rappport = rapport_vgp.list_equipment.split(",")
            for id_equipment in list_ids_equipments_rappport:
                list_audits_equipment = self.env["critt.certification.audit"].search(
                    [
                        ("equipement", "=", int(id_equipment)),
                        ("etat_audit", "=", "termine"),
                    ],
                    order="id desc",
                )
                if list_audits_equipment:
                    audit_avant_rapport = False
                    i = 0
                    while not audit_avant_rapport and i < len(list_audits_equipment):
                        if (
                                list_audits_equipment[i].create_date
                                < rapport_vgp.create_date
                        ):
                            list_audits_rapport.append(str(list_audits_equipment[0].id))
                            audit_avant_rapport = True
                        i += 1
                    if not audit_avant_rapport:
                        # raise ValidationError(_("if not"))
                        list_audits_rapport.append("None")
                else:
                    # raise ValidationError(_("else"))
                    list_audits_rapport.append("None")
            rapport_vgp.list_audits = ",".join(list_audits_rapport)

    def _work_done_on_equipment(self):
        for line in self:
            self.env.cr.execute(
                """SELECT DISTINCT csole.id FROM critt_sale_order_line_equipment as csole 
                    JOIN sale_order so ON csole.order_id = so.id 
                    JOIN critt_equipment e ON csole.equipment_id = e.id 
                    WHERE csole.equipment_id = %s AND e.derniere_facture IS NOT NULL""",
                [self.id],
            )
            ids = [x[0] for x in self.env.cr.fetchall()]
            orderLineEquipment = (
                self.env["critt.sale.order.line.equipment"].sudo().browse(ids)
            )
            line.work_done_on_equipment = orderLineEquipment

    def _compute_rapport_controle(self):
        for line in self:
            rapports_vgp_client = (
                self.env["critt.certification.rapport_controle"]
                    .sudo()
                    .search([("client", "=", self.res_partner_id.id)])
            )
            list_id_rapports_vgp = []
            for rapport_vgp_client in rapports_vgp_client:
                list_equipments_rapport = rapport_vgp_client.list_equipment.split(",")
                if str(self.id) in list_equipments_rapport:
                    list_id_rapports_vgp.append(rapport_vgp_client.id)
            rapport_vgp = (
                self.env["critt.certification.rapport_controle"]
                    .sudo()
                    .search([("id", "in", list_id_rapports_vgp)])
            )
            line.rapport_controle = rapport_vgp

    def _get_referent(self):
        for line in self:
            line.referent2 = None
            if line.referent:
                res = self.env["res.partner"].search(
                    [("id", "=", line.referent.id)], limit=1
                )
                line.referent2 = res

    def action_lancer_diagnostic(self):
        self.ensure_one()
        Audit = self.env["critt.certification.audit"]

        client = self.owner_user_id.partner_id.id
        date = datetime.now()  # .strftime("%d/%m/%Y %H:%M")
        fin = datetime.now() + relativedelta(hours=+1)  # .strftime("%d/%m/%Y %H:%M")
        controleur = (
            self.env["res.users"].search([("id", "=", self.env.uid)]).partner_id.id
        )

        questionnaire = self.env["critt.certification.questionnaire"].search(
            [("categorie", "=", self.category_id.id)],
            limit=1,
            order="date_creation desc",
        )
        if not questionnaire:
            raise ValidationError(
                _("Il n'existe pas de questionnaire pour contrôler ce type de matériel")
            )
        else:
            vals = {
                "client": client,
                "equipement": self.id,
                "questionnaire": questionnaire.id,
                "date": date,
                "fin": fin,
                "id_controleur": controleur,
            }

            audit = Audit.create(vals)

            self.update({"date_dernier_audit": datetime.now()})

            queue = "/%s" % client
            return {
                "type": "ir.actions.act_url",
                "name": "Démarrer questionnaire",
                "target": "self",
                "url": audit.with_context(relative_url=True).url_debuter + queue,
            }

    def action_detruire(self):
        Certificat = self.env["critt.certification.certificat"]
        self.datetime_destruction = datetime.now()
        self.partner_destruct = self.env.user.partner_id.id

        # Création lien certif vue equipements
        # Remplissage du champ pdf
        pdf = "/report/pdf/certification.report_certificat_destruction/" + str(self.id)

        # Remplissage du champ desc
        desc = "Certificat de destruction"

        vals = {
            "desc": desc,
            "pdf": pdf,
            "sequence": 3,
            "id_equipment": self.id,
            "type": "reforme",
        }

        Certificat.create(vals)

        self.certif_destruction = True
        self.statut = "detruit"

    def _is_audit_depasse(self):
        for record in self:
            if record.audit_suivant:
                if datetime.today().date() > record.audit_suivant:
                    record.audit_depasse = True
                else:
                    record.audit_depasse = False
            else:
                record.audit_depasse = True

    def _get_image_photo(self):
        for equipment in self:
            equipment.image_photo = ""
            if equipment.id:
                self.env.cr.execute(
                    "SELECT id FROM ir_attachment WHERE res_id = %s AND res_model = 'critt.equipment' AND name = 'image_medium'",
                    [equipment.id],
                )
                row = self.env.cr.fetchone()
                if row and row[0]:
                    if equipment.image_medium:
                        equipment.image_photo = (
                            equipment.image_medium
                        )
                    else:
                        equipment.image_photo = equipment.image_small

    def _get_image_photo_exist(self):
        for equipment in self:
            equipment.image_photo_exist = False

            self.env.cr.execute(
                "SELECT id FROM ir_attachment WHERE res_id = %s AND res_model = 'critt.equipment' AND name = 'image_small'",
                [equipment.id],
            )
            row = self.env.cr.fetchone()
            if row and row[0]:
                equipment.image_photo_exist = True

    def _get_image_photo2(self):
        for equipment in self:
            equipment.image_photo2 = ""
            if equipment.id:
                self.env.cr.execute(
                    "SELECT id FROM ir_attachment WHERE res_id = %s AND res_model = 'critt.equipment' AND name = 'image_small'",
                    [equipment.id],
                )
                row = self.env.cr.fetchone()
                if row and row[0]:
                    equipment.image_photo2 = equipment.image_medium

    def _get_image_photo_mime_type(self):
        for equipment in self:
            equipment.image_photo_mime_type = "pas ok" + str(equipment.id)
            if equipment.id:
                self.env.cr.execute(
                    "SELECT mimetype FROM ir_attachment WHERE res_id = %s AND res_model = 'critt.equipment' AND name = 'image_small'",
                    [equipment.id],
                )
                row = self.env.cr.fetchone()
                if row and row[0]:
                    equipment.image_photo_mime_type = row[0]

    @api.onchange("category_id")
    def _onchange_category_id(self):
        if self.category_id:
            self.periode = self.category_id.periode

            self.of_cap_levage = self.category_id.of_cap_levage

            if self.date_dernier_audit:
                date = self.date_dernier_audit + relativedelta(
                    months=+int(self.periode)
                )
                self.audit_suivant = date
            else:
                date = datetime.now() + relativedelta(months=+int(self.periode))
                self.audit_suivant = date

            self.display_nombre_brins = self.category_id.display_nombre_brins
            if not self.display_nombre_brins:
                self.nombre_brins = None
            self.display_longueur = self.category_id.display_longueur
            if not self.display_longueur:
                self.longueur = None
            self.display_cmu = self.category_id.display_cmu
            if not self.display_cmu:
                self.cmu = None
            self.display_tmu = self.category_id.display_tmu
            if not self.display_tmu:
                self.tmu = None
            self.display_model = self.category_id.display_model
            if not self.display_model:
                self.model = None
            self.display_diametre = self.category_id.display_diametre
            if not self.display_diametre:
                self.diametre = None
            self.display_grade = self.category_id.display_grade
            if not self.display_grade:
                self.grade = None
            self.display_num_lot = self.category_id.display_num_lot
            if not self.display_num_lot:
                self.num_lot = None
            self.display_num_commande = self.category_id.display_num_commande
            if not self.display_num_commande:
                self.num_commande = None
        else:
            self.periode = ""
            self.display_nombre_brins = False
            self.nombre_brins = None
            self.display_longueur = False
            self.longueur = None
            self.display_cmu = False
            self.cmu = None
            self.display_tmu = False
            self.tmu = None
            self.display_model = False
            self.model = None
            self.display_diametre = False
            self.diametre = None
            self.display_grade = False
            self.grade = None
            self.display_num_lot = False
            self.num_lot = None
            self.display_num_commande = False
            self.num_commande = None

    @api.onchange("periode")
    def _onchange_periode(self):
        for record in self:
            if record.date_dernier_audit:
                date = record.date_dernier_audit + relativedelta(months=+int(record.periode))
                record.audit_suivant = date
            else:
                date = self.an_mise_service + relativedelta(months=+int(record.periode))
                record.audit_suivant = date

    @api.onchange("date_dernier_audit")
    def _onchange_date_dernier_audit(self):
        for record in self:
            if record.date_dernier_audit:
                date = self.date_dernier_audit + relativedelta(months=+int(record.periode))
                record.audit_suivant = date
            else:
                date = self.an_mise_service + relativedelta(months=+int(record.periode))
                record.audit_suivant = date

    @api.onchange("audit_suivant")
    def _onchange_audit_suivant(self):
        for record in self:
            if record.audit_suivant < fields.Date.today() and record.statut == "ok":
                self.action_bloquer()

    @api.model
    def _cron_gerer_etat_materiel(self):
        concerned_equipment = self.search([('audit_suivant', '<', fields.Date.today()), ('statut', '=', 'ok')])
        for materiel in concerned_equipment:
            self.logger.warning(f"CRON - Blocage du matériel {materiel} - {materiel.audit_suivant}")
            materiel.action_bloquer()
        concerned_equipment = self.search([('audit_suivant', '>', fields.Date.today()), ('statut', '=', 'bloque')])
        for materiel in concerned_equipment:
            self.logger.warning(f"CRON - Déblocage du matériel {materiel} - {materiel.audit_suivant}")
            materiel.action_valider()

    def materiel_entre(self):
        self.in_or_out = "in"
        self.date_entree = datetime.now()

    def materiel_sort(self):
        self.in_or_out = "out"
        self.date_sortie = datetime.now()

    @api.onchange("res_partner_id")
    def _onchange_res_partner_id(self):
        self.referent = ""
        self.agence_id = ""
        self.equipe_id = ""
        if self.res_partner_id == "":
            self.owner_user_id = ""
        else:
            self.owner_user_id = self.env["res.users"].search(
                [("partner_id", "=", self.res_partner_id.id)]
            )

    def _count_sale_order(self):
        for equipement in self:
            orders = []
            order_lines = self.env["critt.sale.order.line.equipment"].search(
                [("equipment_id", "=", equipement.id)]
            )
            for order_line in order_lines:
                order = None
                order = self.env["sale.order"].search(
                    [
                        ("id", "=", order_line.order_id.id),
                        ("state", "in", ["draft", "sent"]),
                    ]
                )
                if order:
                    orders.append(order)

            equipement.sale_order_count = len(orders)

    def _count_sale_order_for_portal(self):
        for equipement in self:
            orders = []
            order_lines = self.env["critt.sale.order.line.equipment"].search(
                [("equipment_id", "=", equipement.id)]
            )
            for order_line in order_lines:
                order = None
                order = self.env["sale.order"].search(
                    [("id", "=", order_line.order_id.id), ("state", "in", ["sent"])]
                )
                if order:
                    orders.append(order)

            equipement.sale_order_count_for_portal = len(orders)

    def _get_audit_suivant_color(self):
        for equipment in self:
            if equipment.audit_suivant:
                equipment.audit_suivant_color = ""
                year = int(equipment.audit_suivant.strftime("%Y"))
                month = int(equipment.audit_suivant.strftime("%m"))
                day = int(equipment.audit_suivant.strftime("%d"))
                duree = datetime(year, month, day) - datetime.now()
                # delta = a - now
                if duree.days < 0:
                    equipment.audit_suivant_color = "red"
                elif duree.days <= 31:
                    equipment.audit_suivant_color = "orange"
                else:
                    equipment.audit_suivant_color = ""
            else:
                equipment.audit_suivant_color = ""

    def _get_audit_suivant_color_index(self):
        for equipment in self:
            equipment.audit_suivant_color_index = 0
            if equipment.audit_suivant:
                year = int(equipment.audit_suivant.strftime("%Y"))
                month = int(equipment.audit_suivant.strftime("%m"))
                day = int(equipment.audit_suivant.strftime("%d"))
                duree = datetime(year, month, day) - datetime.now()
                if duree.days < 0:
                    equipment.audit_suivant_color_index = 1
                elif duree.days <= 31:
                    equipment.audit_suivant_color_index = 2

    def _get_date_last_audit_string(self):
        for equipment in self:
            self.env.cr.execute(
                "SELECT date FROM critt_certification_audit WHERE equipement = %s AND etat_audit IN('termine') ORDER BY fin DESC",
                [equipment.id],
            )
            row = self.env.cr.fetchone()
            if row and row[0]:
                equipment.date_last_audit_string = (
                    datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                        .date()
                        .strftime("%d/%m/%Y")
                )
            else:
                equipment.date_last_audit_string = ""

    def _get_date_last_audit(self):
        for equipment in self:
            self.env.cr.execute(
                "SELECT date FROM critt_certification_audit WHERE equipement = %s AND etat_audit IN('termine') ORDER BY fin DESC",
                [equipment.id],
            )
            row = self.env.cr.fetchone()
            if row and row[0]:
                equipment.date_last_audit = (
                    datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                        .date()
                        .strftime("%d/%m/%Y")
                )
            else:
                equipment.date_last_audit = ""

    def _get_last_audit(self):
        for equipment in self:
            equipment.last_audit = -1
            audits = self.env["critt.certification.audit"].search(
                [("equipement", "=", equipment.id)], limit=1, order="fin desc"
            )
            if audits:
                if audits[0].acces_certif:
                    equipment.last_audit = audits[0].id

    def _get_last_certificat(self):
        for equipment in self:
            equipment.last_certificat = ""
            certificats = self.env["critt.certification.certificat"].search(
                [("id_equipment", "=", equipment.id), ("pdf", "!=", None)],
                limit=1,
                order="create_date desc",
            )
            if certificats:
                if certificats[0].type in ["creation", "reforme"]:
                    equipment.last_certificat = certificats[0].pdf
                else:
                    if certificats[0].id_audit.acces_certif:
                        equipment.last_certificat = certificats[0].pdf

    def _get_statut_libelle(self):
        for equipment in self:
            equipment.statut_libelle = dict(self._fields["statut"].selection).get(
                equipment.statut
            )

    def _get_statut_index(self):
        for equipment in self:
            if equipment.statut == "ok":
                equipment.statut_index = 0
            elif equipment.statut == "en_cours":
                equipment.statut_index = 1
            elif equipment.statut == "bloque":
                equipment.statut_index = 2
            elif equipment.statut == "reforme" or equipment.statut == "detruit":
                equipment.statut_index = 3
            else:
                equipment.statut_index = -1

    def map(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://maps.google.com/?q=%s,%s" % (self.latitude, self.longitude),
            # 'url': 'https://www.google.fr/maps/@%s,%sz' % (self.latitude, self.longitude),
            "target": "_blank",
        }

    # gestion image
    @api.model
    def create(self, vals):
        Certificat = self.env["critt.certification.certificat"]
        partner_create = (
            self.env["res.users"].search([("id", "=", self.env.uid)]).partner_id.id
        )
        vals.update({"partner_create": partner_create})

        if vals.get("qr_code"):
            qr_code = vals.get("qr_code")
            equipment_qr_code = self.env["critt.equipment"].search(
                [("qr_code", "=", qr_code)]
            )
            if equipment_qr_code:
                raise ValidationError(_("Ce QR Code à déjà été affecté"))

        equipment = super(MaintenanceEquipment, self).create(vals)

        if equipment.is_new and equipment.from_cap_levage:
            # Création lien certif vue equipements
            # Remplissage du champ pdf
            pdf = "/report/pdf/certification.report_certificat_creation/" + str(
                equipment.id
            )

            date = datetime.now().date()

            # Remplissage du champ desc
            desc = "Certificat de fabrication"

            vals2 = {
                "desc": desc,
                "pdf": pdf,
                "id_equipment": equipment.id,
                "type": "creation",
                "date": date,
                "sequence": 1,
            }

            Certificat.create(vals2)
            equipment.certif_creation = True

        if vals.get("qr_code"):
            Horodating = self.env["critt.horodating"]

            vals = {
                "user": self.env.user.id,
                "action": "Affectation QR Code",
                "equipment_id": equipment.id,
            }

            Horodating.create(vals)

        return equipment

    def write(self, vals):

        if vals.get("qr_code"):
            qr_code = vals.get("qr_code")
            equipment_qr_code = self.env["critt.equipment"].search(
                [("qr_code", "=", qr_code), ("id", "!=", self.id)]
            )
            if equipment_qr_code:
                raise ValidationError(
                    _("Ce QR Code a déjà été affecté " + str(equipment_qr_code.id))
                )

            Horodating = self.env["critt.horodating"]
            old_equipment_qr = self.qr_code

            if old_equipment_qr:
                vals2 = {
                    "user": self.env.user.id,
                    "action": "Modification QR Code",
                    "equipment_id": self.id,
                }
            else:
                vals2 = {
                    "user": self.env.user.id,
                    "action": "Affectation QR Code",
                    "equipment_id": self.id,
                }

            Horodating.create(vals2)

        if self.is_duplicated:
            vals.update({"date_dernier_audit": datetime.now(), "is_duplicated": False})

        if self.audit_suivant and self.audit_suivant < fields.Date.today():
            vals.update({"statut": "bloque"})

        return super(MaintenanceEquipment, self).write(vals)

    def copy(self, default=None):
        default = dict(default or {})

        default.update({"num_materiel": "duplication_"})

        maintenance_equipment = super(MaintenanceEquipment, self).copy(default)
        maintenance_equipment.update(
            {
                "num_materiel": "duplication_" + str(maintenance_equipment.id),
                "is_duplicated": True,
            }
        )
        return maintenance_equipment

    @api.onchange("of_cap_levage")
    def _onchange_of_cap_levage(self):
        if self.of_cap_levage:
            self.orga_certif = "Cap Levage"
        else:
            self.orga_certif = ""

    def voir_devis(self):
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            vue_devis_tree = ir_model_data.get_object_reference(
                "certification", "vue_sale_order_tree"
            )[1]
            vue_devis_form = ir_model_data.get_object_reference(
                "sale", "view_order_form"
            )[1]
        except ValueError:
            vue_devis_tree = False
            vue_devis_form = False

        orders = []
        order_lines = self.env["critt.sale.order.line.equipment"].search(
            [("equipment_id", "=", self.id)]
        )
        for order_line in order_lines:
            order = None
            order = self.env["sale.order"].search([("id", "=", order_line.order_id.id)])
            if order:
                orders.append(order.id)

        return {
            "name": self.num_materiel,
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "views": [(vue_devis_tree, "tree"), (vue_devis_form, "form")],
            "view_id": vue_devis_tree,
            "target": "current",
            "domain": "[('id', 'in', %s), ('state', 'in', ['draft','sent'])]" % orders,
        }

    def action_creer_audit(self):
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            vue_audit_form = ir_model_data.get_object_reference(
                "certification", "vue_audit_form"
            )[1]
        except ValueError:
            vue_audit_form = False

        ctx = {
            "default_client": self.owner_user_id.partner_id.id,
            "default_equipement": self.id,
            "default_date": datetime.now(),
            "default_fin": datetime.now() + relativedelta(hours=+1),
        }

        return {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "critt.certification.audit",
            "views": [(vue_audit_form, "form")],
            "view_id": vue_audit_form,
            "target": "current",
            "context": ctx,
        }

    def action_creer_devis(self):
        SaleOrderLineEquipement = self.env["critt.sale.order.line.equipment"]
        SaleOrder = self.env["sale.order"]
        # SaleOrderLine = self.env['sale.order.line']
        #     self.ensure_one()
        #     ir_model_data = self.env['ir.model.data']
        #     try:
        #         vue_devis_form = ir_model_data.get_object_reference('certification', 'vue_sale_order_form')[1]
        #     except ValueError:
        #         vue_devis_form = False
        #

        vals = {"partner_id": self.owner_user_id.partner_id.id, "state": "draft"}
        saleorder = SaleOrder.create(vals)

        vals = {"order_id": saleorder.id, "equipment_id": self.id}
        SaleOrderLineEquipement.create(vals)

        # service = self.env['product.template'].search([('categ_id', '=', self.category_id.category_article_id.id), ('type', '=', 'service')])
        # if service:
        #     vals = {'product_id': service.id, 'order_id': saleorder.id}
        #     ligne_cout_audit = self.env['critt.certification.cout_audit'].search([('id_client', '=', self.owner_user_id.partner_id.id), ('categorie_equipement', '=', self.category_id.id)], limit=1)
        #     if ligne_cout_audit.cout and ligne_cout_audit.cout != 0:
        #         price = ligne_cout_audit.cout
        #         vals.update({'price_unit': price})
        #
        #     SaleOrderLine.create(vals)

        return saleorder.id

    def action_voir_devis(self):
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            vue_devis_form = ir_model_data.get_object_reference(
                "certification", "vue_devis_form"
            )[1]
        except ValueError:
            vue_devis_form = False

        last_order_line_equipement = self.env["critt.sale.order.line.equipment"].search(
            [("equipment_id", "=", self.id)], order="create_date desc", limit=1
        )
        last_order = self.env["sale.order"].search(
            [("id", "=", last_order_line_equipement.order_id.id)]
        )

        return {
            "type": "ir_actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": last_order.id,
            "views": [(vue_devis_form, "form")],
            "view_id": vue_devis_form,
            "target": "current",
        }

    def action_voir_audit(self):
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            vue_audit_form = ir_model_data.get_object_reference(
                "certification", "vue_audit_form"
            )[1]
        except ValueError:
            vue_audit_form = False

        last_audit = self.env["critt.certification.audit"].search(
            [("equipement", "=", self.id)], order="date desc", limit=1
        )

        return {
            "type": "ir_actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "critt.certification.audit",
            "res_id": last_audit.id,
            "views": [(vue_audit_form, "form")],
            "view_id": vue_audit_form,
            "target": "current",
        }

    def materiel_repare(self, context):
        selected_ids = context.get("active_ids", False)

        # Récupération devis sélectionnés
        list_devis = []
        for item in selected_ids:
            devis = self.env["sale.order"].search([("id", "=", item)])
            list_devis.append(devis)

        # Récupération équipements concernés
        for devis in list_devis:
            equipment = (
                self.env["critt.sale.order.line.equipment"]
                    .search([("order_id", "=", devis.id)])
                    .equipment_id
            )
            equipment.update({"statut": "ok"})

            # Création lien certif vue equipements
            # Recherche dernier audit
            last_audit = self.env["critt.certification.audit"].search(
                [("equipement", "=", equipment.id)], limit=1, order="id desc"
            )

            # Remplissage du champ pdf
            pdf = "/report/pdf/certification.report_certificat_conforme/" + str(
                last_audit.id
            )

            # Remplissage du champ date
            split_1_date = last_audit.date.split()
            split_2_date = split_1_date[0].split("-")
            date = split_2_date[1] + "/" + split_2_date[0]

            # Remplissage du champ desc
            desc = "Contrôle du " + date

            vals2 = {
                "desc": desc,
                "date": date,
                "pdf": pdf,
                "id_audit": last_audit.id,
                "id_equipment": equipment.id,
                "type": "controle",
                "sequence": 2,
            }

            self.env["critt.certification.certificat"].create(vals2)
            last_audit.certif_conforme = True

    def materiel_reforme(self, context):
        selected_ids = context.get("active_ids", False)

        # Récupération devis sélectionnés
        list_devis = []
        for item in selected_ids:
            devis = self.env["sale.order"].search([("id", "=", item)])
            list_devis.append(devis)

        # Récupération équipements concernés
        for devis in list_devis:
            equipment = (
                self.env["critt.sale.order.line.equipment"]
                    .search([("order_id", "=", devis.id)])
                    .equipment_id
            )
            equipment.update({"statut": "reforme", "audit_suivant": None})

    _sql_constraints = [
        (
            "unique_num_materiel",
            "UNIQUE(num_materiel)",
            "Ce numéro de matériel existe déjà",
        ),
    ]


class EquipmentCategory(models.Model):
    _name = "critt.equipment.category"

    name = fields.Char(string="Nom", required=True)
    technician_user_id = fields.Many2one(
        "res.users",
        "Responsable",
        track_visibility="onchange",
        default=lambda self: self.env.uid,
        oldname="user_id",
    )
    color = fields.Integer("Color Index")
    # note = fields.Text('Comments', translate=True)
    equipment_ids = fields.One2many(
        "critt.equipment", "category_id", string="Equipments", copy=False
    )
    equipment_count = fields.Integer(
        string="Equipment", compute="_compute_equipment_count"
    )

    periode = fields.Integer(
        string="Periodicite des audits (en mois)", required=True, default=0
    )

    image = fields.Binary(string="Image")
    url_video = fields.Char(string="Lien vidéo")

    coef_secu = fields.Integer(string="Coefficient de sécurité")

    of_cap_levage = fields.Boolean(string="Gérée par Cap Levage", default=False)
    display_nombre_brins = fields.Boolean(
        string="Afficher le champ nombre de brins", default=False
    )
    display_longueur = fields.Boolean(
        string="Afficher le champ longueur", default=False
    )
    display_cmu = fields.Boolean(string="Afficher le champ CMU", default=False)
    display_tmu = fields.Boolean(string="Afficher le champ TMU", default=False)
    display_model = fields.Boolean(string="Afficher le champ modèle", default=False)
    display_diametre = fields.Boolean(
        string="Afficher le champ diamètre", default=False
    )
    display_grade = fields.Boolean(string="Afficher le champ grade", default=False)
    display_num_lot = fields.Boolean(
        string="Afficher le champ numéro de lot", default=False
    )
    display_num_commande = fields.Boolean(
        string="Afficher le champ numéro de commande", default=False
    )

    category_article_id = fields.Many2one(
        "product.category", "Catégorie produit", required=True
    )

    equipment_create_right_ids = fields.One2many(
        "critt.equipment.create_right", "category_id", string="Clients autorisés"
    )

    def write(self, vals):
        category = super(EquipmentCategory, self).write(vals)

        liste_mat_update = self.env["critt.equipment"].search(
            [("category_id", "=", self.id)]
        )
        for mat_update in liste_mat_update:
            mat_update.display_nombre_brins = self.display_nombre_brins
            if not self.display_nombre_brins:
                mat_update.nombre_brins = None
            mat_update.display_longueur = self.display_longueur
            if not self.display_longueur:
                mat_update.longueur = None
            mat_update.display_cmu = self.display_cmu
            if not self.display_cmu:
                mat_update.cmu = None
            mat_update.display_tmu = self.display_tmu
            if not self.display_tmu:
                mat_update.tmu = None
            mat_update.of_cap_levage = self.of_cap_levage
            # if self.of_cap_levage:
            #     mat_update.orga_certif = "Cap Levage"
            # else:
            #     mat_update.orga_certif = "Autre"
            mat_update.display_diametre = self.display_diametre
            if not self.display_diametre:
                mat_update.diametre = None
            mat_update.display_grade = self.display_grade
            if not self.display_grade:
                mat_update.grade = None
            mat_update.display_num_lot = self.display_num_lot
            if not self.display_num_lot:
                mat_update.num_lot = None
            mat_update.display_num_commande = self.display_num_commande
            if not self.display_num_commande:
                mat_update.num_commande = None

        return category

    def _compute_equipment_count(self):
        equipment_data = self.env["critt.equipment"].read_group(
            [("category_id", "in", self.ids)], ["category_id"], ["category_id"]
        )
        mapped_data = dict(
            [(m["category_id"][0], m["category_id_count"]) for m in equipment_data]
        )
        for category in self:
            category.equipment_count = mapped_data.get(category.id, 0)

    def unlink(self):
        equipment = self.env["critt.equipment"].search([("category_id", "=", self.id)])
        if len(equipment) > 0:
            raise ValidationError(
                _(
                    "Vous ne pouvez pas supprimer une catégorie contenant des équipements"
                )
            )
        return super(EquipmentCategory, self).unlink()


class OrganismeCertification(models.Model):
    _name = "critt.equipment.organisme"

    name = fields.Char(string="Nom", required=True)

    equipment_ids = fields.One2many(
        "critt.equipment", "organisme_id", string="Equipments", copy=False
    )


class Fabricant(models.Model):
    _name = "critt.equipment.fabricant"

    name = fields.Char(string="Nom", required=True)

    equipment_ids = fields.One2many(
        "critt.equipment", "fabricant_id", string="Equipments", copy=False
    )


class IrAttachment(models.Model):
    _name = "ir.attachment"
    _inherit = "ir.attachment"

    certificat_date = fields.Datetime("Date Certificat")

    orga_certif = fields.Char(string="Organisme certifiant")

    type_certificat = fields.Selection(
        [("creation", "Création"), ("controle", "Contrôle"), ("reforme", "Réforme")],
        string="Type",
        default="",
    )

    sequence_certificat = fields.Integer(string="Sequence")

    @api.model
    def create(self, vals):
        if (
                vals.get("res_model") == "critt.equipment"
                and vals.get("res_field") == "image_medium"
        ):
            compressed_image = self.compressImage(vals.get("datas"))
            ir_attachment = super(IrAttachment, self).create(vals)
            # vals_img_small = {'name': 'image_small', 'res_model': 'critt.equipment', 'res_field': 'image_small',
            #                  'res_id': ir_attachment.res_id, 'type': 'binary', 'datas_fname': self.store_fname,
            #                  'datas': compressed_image}
            vals_img_small = {
                "name": "image_small",
                "res_model": "critt.equipment",
                "res_field": "image_small",
                "res_id": ir_attachment.res_id,
                "type": "binary",
                "datas": compressed_image,
            }
            self.create(vals_img_small)
            return ir_attachment
        else:
            return super(IrAttachment, self).create(vals)

    def write(self, vals):
        for rec in self:
            if rec.res_model == "critt.equipment" and rec.res_field == "image_medium":
                compressed_image = self.compressImage(vals.get("datas"))
                old = self.env["ir.attachment"].search(
                    [
                        ("res_model", "=", "critt.equipment"),
                        ("res_field", "=", "image_small"),
                        ("res_id", "=", rec.res_id),
                    ]
                )
                old.unlink()
                vals_img_small = {
                    "name": "image_small",
                    "res_model": "critt.equipment",
                    "res_field": "image_small",
                    "res_id": rec.res_id,
                    "type": "binary",
                    "datas": compressed_image,
                }
                self.create(vals_img_small)
        return super(IrAttachment, self).write(vals)

    def compressImage(self, image):
        to_compress = tools.base64_to_image(image)
        max_size = 100
        wpercent = max_size / float(to_compress.size[0])
        hpercent = max_size / float(to_compress.size[1])
        if wpercent < hpercent:
            hsize = int((float(to_compress.size[1]) * float(wpercent)))
            compressed = to_compress.resize((max_size, hsize), Image.ANTIALIAS)
        if wpercent > hpercent:
            wsize = int((float(to_compress.size[0]) * float(hpercent)))
            compressed = to_compress.resize((wsize, max_size), Image.ANTIALIAS)
        if wpercent == hpercent:
            compressed = to_compress.resize((max_size, max_size), Image.ANTIALIAS)
        b64_image = tools.image_to_base64(compressed, "JPEG")
        return b64_image


class EquipmentCreateRight(models.Model):
    _name = "critt.equipment.create_right"

    category_id = fields.Many2one(
        "critt.equipment.category", string="Catégorie", required=True
    )
    res_partner_id = fields.Many2one("res.partner", string="Client", required=True)
