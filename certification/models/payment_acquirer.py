from odoo import api, models, fields
from odoo.tools import consteq, float_round, ustr
import os


class inherit_payment_transaction(models.Model):
    _name = "payment.transaction"
    _inherit = "payment.transaction"

    @api.model
    def create(self, values):
        if values.get("partner_id"):  # @TDENOTE: not sure
            values.update(self.on_change_partner_id(values["partner_id"])["value"])

        # call custom create method if defined (i.e. ogone_create for ogone)
        if values.get("acquirer_id"):
            acquirer = self.env["payment.acquirer"].browse(values["acquirer_id"])

            # compute fees
            custom_method_name = "%s_compute_fees" % acquirer.provider
            if hasattr(acquirer, custom_method_name):
                fees = getattr(acquirer, custom_method_name)(
                    values.get("amount", 0.0),
                    values.get("currency_id"),
                    values.get("partner_country_id"),
                )
                values["fees"] = float_round(fees, 2)

            # custom create
            custom_method_name = "%s_create" % acquirer.provider
            if hasattr(acquirer, custom_method_name):
                values.update(getattr(self, custom_method_name)(values))

        # Default value of reference is
        tx = super(inherit_payment_transaction, self).create(values)
        if not values.get("reference"):
            tx.write({"reference": str(tx.id)})

        # Generate callback hash if it is configured on the tx; avoid generating unnecessary stuff
        # (limited sudo env for checking callback presence, must work for manual transactions too)
        tx_sudo = tx.sudo()
        if (
            tx_sudo.callback_model_id
            and tx_sudo.callback_res_id
            and tx_sudo.callback_method
        ):
            tx.write({"callback_hash": tx._generate_callback_hash()})

        # add by critt: create equipment with product after payment (obsolète)
        # sale_order = self.env['sale.order'].browse(values['sale_order_id'])
        # partner = sale_order.partner_id
        # User = self.env['res.users'].search([('partner_id', '=', partner.id)])
        # if User:
        # self.env.cr.execute("SELECT id FROM sale_order_line WHERE order_id = %s", [sale_order.id])
        # saleOrderLines = self.env.cr.fetchall()

        # for line in saleOrderLines:
        # saleOrderLine = self.env['sale.order.line'].browse(line[0])
        # for i in range(0, int(saleOrderLine.product_uom_qty)):
        # if saleOrderLine.product_id.product_tmpl_id.type not in ['service']:
        # self._createEquipment(saleOrderLine.product_id, User.id)

        return tx

    def _createEquipment(self, product, user_id):
        category_id = product.categ_id

        self.env.cr.execute(
            "SELECT count(*) FROM critt_equipment_category WHERE name = %s",
            [category_id.name],
        )
        categories = self.env.cr.fetchall()
        # if not exist, create category equipment
        if int(categories[0][0]) == 0:
            categ = self.env["critt.equipment.category"]
            done = self.env["critt.equipment.category"].browse()
            template = {"name": category_id.name, "category_article_id": category_id.id}
            newCateg = categ.create(template)
            category_id = newCateg.id
            done += newCateg
        else:
            self.env.cr.execute(
                "SELECT id FROM critt_equipment_category WHERE name = %s",
                [category_id.name],
            )
            category_id = self.env.cr.fetchone()[0]

        # self.env.cr.execute("SELECT count(*) FROM maintenance_equipment WHERE name = %s", [product.name])
        # equipments = self.env.cr.fetchall()
        # if not exist, create

        # newEquip = -1
        # if int(equipments[0][0]) == 0:
        equip = self.env["critt.equipment"]
        done = self.env["critt.equipment"].browse()
        template = {
            "name": product.name,
            "category_id": category_id,
            "owner_user_id": user_id,  # self.env.user.id
            #'orga_certif': '',
            "periode": 0,
            "statut": "ok",
            "orga_certif": "Cap Levage",
            "of_cap_levage": True,
        }
        newEquip = equip.create(template)
        done += newEquip

        # duplicate image if new equipment
        # if newEquip != -1:
        self.env.cr.execute(
            "SELECT id FROM ir_attachment WHERE res_id = %s AND res_model = 'product.template'",
            [product.product_tmpl_id.id],
        )
        images = self.env.cr.fetchall()
        for item in images:
            image = self.env["ir.attachment"].browse(int(item[0]))
            image.copy(
                default={
                    "res_id": newEquip.id,
                    "res_model": "critt.equipment",
                    "res_name": product.name,
                }
            )
