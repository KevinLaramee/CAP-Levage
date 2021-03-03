import logging

from ast import literal_eval

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import ustr

# from odoo.addons.base.ir.ir_mail_server import MailDeliveryException
from odoo.addons.auth_signup.models.res_partner import SignupError, now
from datetime import datetime


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    order_line_equipment = fields.One2many(
        "critt.sale.order.line.equipment",
        "order_id",
        string="Order Lines Equipment",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
        copy=True,
        auto_join=True,
    )

    invoice = fields.Many2one(
        "account.move",
        string="Invoices",
        compute="_get_invoice",
        readonly=True,
        copy=False,
    )

    # state = fields.Selection(selection_add=[('model', 'Modèle')])

    # is_model = fields.Boolean(string="Est un modèle de devis", default=False)

    # type_materiel_id = fields.Many2one("critt.equipment.category", string="Type d'équipement")

    state_libelle = fields.Char(
        "Libellé état", compute="_get_state_libelle", copy=False
    )

    num_commande_client = fields.Char(string="N° de commande client")

    # partner_name = fields.Char(string="Client", compute="_get_partner_name")

    is_validate_by_customer = fields.Boolean(
        string="Validé par le client", default=False
    )

    bon_de_commande_client = fields.Char(
        string="Bon de commande", compute="_get_bon_de_commande_client"
    )

    num_commande_client_required = fields.Boolean(
        string="N° de commande obligatoire", compute="_num_commande_client_required"
    )

    # ajouter de tag_ids et opportunity_id from sale_crm sinon erreur pour afficher le module ventes liste devis depuis l'ajout de la gestion des droits
    tag_ids = fields.Many2many(
        "crm.lead.tag", "sale_order_tag_rel", "order_id", "tag_id", string="Tags"
    )
    opportunity_id = fields.Many2one(
        "crm.lead",
        string="Opportunity",
        check_company=True,
        domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    # def _get_partner_name(self):
    #     for order in self:
    #         order.partner_name = order.partner_id.company_name

    def _get_invoice(self):
        for order in self:
            order.invoice = self.env["account.move"].search(
                [("invoice_origin", "=", order.name)]
            )

    def _get_bon_de_commande_client(self):
        for order in self:
            order.bon_de_commande_client = ""
            try:
                self.env.cr.execute(
                    "SELECT DISTINCT id FROM ir_attachment WHERE res_model = 'sale.order' AND res_id = %s AND description = 'Bon de commande client'",
                    [order.id],
                )
                attachement_ids = [x[0] for x in self.env.cr.fetchall()]
                for attachement_id in attachement_ids:
                    # attachment = self.env['ir.attachment'].browse(int(attachement_id))
                    order.bon_de_commande_client = (
                        "/web/content/%s?download=1" % attachement_id
                    )

                # id_ir_attachment = self.env['ir.attachment'].search([('res_model', '=', 'critt.certification.certificat'), ('res_id', '=', certificat.id)])
                # certificat.dl_pdf = "/web/content/%s/%s?download=1" % (id_ir_attachment, certificat.id)
            except:
                order.bon_de_commande_client = "error"

    def _num_commande_client_required(self):
        for order in self:
            if order.partner_id:
                order.num_commande_client_required = (
                    order.partner_id.num_commande_client_required
                )
            else:
                order.num_commande_client_required = False

    def _get_state_libelle(self):
        for order in self:
            order.state_libelle = ""
            if order.state == "draft":
                order.state_libelle = "En cours de traitement"
            if order.state == "sent":
                order.state_libelle = "Devis envoyé"
            if order.state == "sale":
                order.state_libelle = "Bon de commande"
            if order.state == "done":
                order.state_libelle = "Terminée"
            if order.state == "cancel":
                order.state_libelle = "Annulée"
            # order.state_libelle = dict(self._fields['state'].selection).get(order.state)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            if "company_id" in vals:
                vals["name"] = self.env["ir.sequence"].with_context(
                    force_company=vals["company_id"]
                ).next_by_code("sale.order") or _("New")
            else:
                vals["name"] = self.env["ir.sequence"].next_by_code("sale.order") or _(
                    "New"
                )

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(
            f not in vals
            for f in ["partner_invoice_id", "partner_shipping_id", "pricelist_id"]
        ):
            partner = self.env["res.partner"].browse(vals.get("partner_id"))
            addr = partner.address_get(["delivery", "invoice"])
            vals["partner_invoice_id"] = vals.setdefault(
                "partner_invoice_id", addr["invoice"]
            )
            vals["partner_shipping_id"] = vals.setdefault(
                "partner_shipping_id", addr["delivery"]
            )
            vals["pricelist_id"] = vals.setdefault(
                "pricelist_id",
                partner.property_product_pricelist
                and partner.property_product_pricelist.id,
            )

        vals["user_id"] = None
        result = super(SaleOrderInherit, self).create(vals)

        # change statut equipment
        self.env.cr.execute(
            "SELECT equipment_id FROM critt_sale_order_line_equipment WHERE order_id = %s",
            [result.id],
        )
        rows = self.env.cr.fetchall()
        for row in rows:
            equipment = self.env["critt.equipment"].search([("id", "=", int(row[0]))])
            if equipment:
                template = {"statut": "en_cours"}  #'audit_a_faire'
                equipment.write(template)

        return result


class SaleOrderLineEquipment(models.Model):
    _name = "critt.sale.order.line.equipment"

    order_id = fields.Many2one(
        "sale.order",
        string="Ordre de réparation",
        required=True,
        ondelete="cascade",
        index=True,
        copy=False,
    )
    equipment_id = fields.Many2one(
        "critt.equipment", string="Matériel", ondelete="restrict", required=True
    )

    last_work_year = fields.Char(string="Année", compute="_get_last_work_year")
    last_work_num_facture = fields.Char(string="N° Facture", compute="_get_num_facture")
    last_work_pdf = fields.Char(string="N° Facture", compute="_get_pdf")

    # invoice_ok = fields.Boolean(string="N° Facture", compute="_get_test")
    invoice_ok = fields.Boolean(string="Facture", default=False, compute="_get_test")

    def _get_num_facture(self):
        for line in self:
            line.last_work_num_facture = ""
            if line.order_id.invoice:
                line.last_work_num_facture = line.order_id.invoice.name

    def _get_last_work_year(self):
        for line in self:
            line.last_work_year = ""
            if line.order_id.invoice:
                line.last_work_year = line.order_id.invoice.date.strftime("%Y")

    def _get_pdf(self):
        for line in self:
            line.last_work_pdf = ""
            if line.order_id.invoice:
                line.last_work_pdf = "/report/html/account.report_invoice/" + str(
                    line.order_id.invoice.id
                )

    def _get_test(self):
        for line in self:
            line.invoice_ok = False
            if line.order_id.invoice:
                line.invoice_ok = True

    def play_file(self):
        if self.order_id.invoice:
            return {
                "type": "ir.actions.act_url",
                "url": "/report/html/account.report_invoice/"
                + str(self.order_id.invoice.id),
            }
        return {"type": "ir.actions.act_url", "url": ""}
