from odoo import api, models, fields, tools
from odoo.tools import pycompat
from datetime import time, datetime, date

from odoo.exceptions import UserError, ValidationError
from odoo import SUPERUSER_ID


class PartnerInherit(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    first_name = fields.Char("Prénom")
    last_name = fields.Char("Nom")
    portal_authorized = fields.Boolean(string="Accès site web", default=True)
    is_customer = fields.Boolean(string="Est un client", default=True)

    context_parent_id = fields.Many2one("res.partner", "Contexte parent_id")

    image_photo = fields.Char("image_photo", compute="_get_image_photo", copy=False)

    ids_equipements = fields.One2many(
        "critt.equipment",
        "owner_user_id",
        string="Equipements possédés",
        compute="_get_list_equipments",
    )

    ids_rapport_controle = fields.One2many(
        "critt.certification.rapport_controle",
        "client",
        string="Rapports de contrôle",
        compute="_get_list_rapport_controle",
    )

    dao = fields.Boolean(string="Service DAO")
    gest_materiel = fields.Boolean(string="Gestion matériel")
    date_fin_essai = fields.Date(string="Fin de version d'essai")

    equipe_id = fields.Many2one(
        "res.partner", string="Équipe", domain="[('type', '=', 'contact')]"
    )
    agence_id = fields.Many2one(
        "res.partner", string="Agence", domain="[('type', '=', 'delivery')]"
    )
    audits_realises = fields.One2many(
        "critt.certification.audit", "id_controleur", string="Audits réalisés"
    )

    signature = fields.Binary(string="Signature")

    equipment_create_right_ids = fields.One2many(
        "critt.equipment.create_right", "res_partner_id", string="Catégories autorisées"
    )

    has_account = fields.Boolean(string="Possède un compte", default=False)

    num_commande_client_required = fields.Boolean(string="N° de commande obligatoire")

    def _get_list_equipments(self):
        for rec in self:
            self.env.cr.execute(
                "SELECT id FROM res_users WHERE partner_id = %s", [rec.id]
            )
            row = self.env.cr.fetchone()
            if row and row[0]:
                self.env.cr.execute(
                    "SELECT DISTINCT id FROM critt_equipment " "WHERE owner_user_id=%s",
                    (row[0],),
                )
                ids = [x[0] for x in self.env.cr.fetchall()]
                equipments = self.env["critt.equipment"].sudo().browse(ids)
                rec.ids_equipements = equipments
            else:
                self.env.cr.execute(
                    "SELECT DISTINCT id FROM critt_equipment WHERE id = -1"
                )
                ids = [x[0] for x in self.env.cr.fetchall()]
                equipments = self.env["critt.equipment"].sudo().browse(ids)
                rec.ids_equipements = equipments

    def _get_list_rapport_controle(self):
        for rec in self:
            related_recordset = self.env["critt.certification.rapport_controle"].search(
                [("client", "=", rec.id)]
            )
            rec.ids_rapport_controle = related_recordset

    # gestion image

    def _get_image_photo(self):
        for partner in self:
            partner.image_photo = ""
            if partner.id:
                self.env.cr.execute(
                    "SELECT id FROM ir_attachment WHERE res_id = %s AND res_model = 'res.partner' AND name = 'image_medium'",
                    [partner.id],
                )
                row = self.env.cr.fetchone()
                if row and row[0]:
                    partner.image_photo = (
                        "/web/image?model=res.partner&id="
                        + str(partner.id)
                        + "&field=image_medium"
                    )

    @api.onchange("company_name")
    def _onchange_company_name(self):
        if self.company_name == "":
            self.name = ""
        else:
            self.name = self.company_name

    @api.onchange("context_parent_id")
    def _onchange_context_parent_id(self):
        if self.context_parent_id != "":
            self.parent_id = self.context_parent_id

    def write(self, vals):
        # res.partner must only allow to set the company_id of a partner if it
        # is the same as the company of all users that inherit from this partner
        # (this is to allow the code from res_users to write to the partner!) or
        # if setting the company_id to False (this is compatible with any user
        # company)
        if vals.get("website"):
            vals["website"] = self._clean_website(vals["website"])
        if vals.get("parent_id"):
            vals["company_name"] = False
        if vals.get("company_id"):
            company = self.env["res.company"].browse(vals["company_id"])
            for partner in self:
                if partner.user_ids:
                    companies = set(user.company_id for user in partner.user_ids)
                    if len(companies) > 1 or company not in companies:
                        raise UserError(
                            _(
                                "You can not change the company as the partner/user has multiple user linked with different companies."
                            )
                        )
        # tools.image_resize_images(vals)

        result = True
        # To write in SUPERUSER on field is_company and avoid access rights problems.
        if (
            "is_company" in vals
            and self.user_has_groups("base.group_partner_manager")
            and not self.env.uid == SUPERUSER_ID
        ):
            result = super(PartnerInherit, self.sudo()).write(
                {"is_company": vals.get("is_company")}
            )
            del vals["is_company"]
        result = result and super(PartnerInherit, self).write(vals)
        for partner in self:
            if any(
                u.has_group("base.group_user")
                for u in partner.user_ids
                if u != self.env.user
            ):
                self.env["res.users"].check_access_rights("write")
            partner._fields_sync(vals)

        return result

    @api.model
    def create(self, vals):
        if vals.get("website"):
            vals["website"] = self._clean_website(vals["website"])
        if vals.get("parent_id"):
            vals["company_name"] = False

        partner = super(PartnerInherit, self).create(vals)
        partner._fields_sync(vals)
        partner._handle_first_contact_creation()

        return partner

    def unlink(self):
        user = self.env["res.users"].search([("partner_id", "=", self.id)])
        if user:
            user.unlink()

        return super(PartnerInherit, self).unlink()
