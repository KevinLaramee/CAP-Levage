import logging

from ast import literal_eval

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import ustr

# from odoo.addons.base.ir.ir_mail_server import MailDeliveryException
from odoo.addons.auth_signup.models.res_partner import SignupError, now
from datetime import datetime


class ResUsers(models.Model):
    _inherit = "res.users"

    equipments = fields.One2many("critt.equipment", "owner_user_id")
    # internal_user = fields.Boolean('Utilisateur interne')
    #
    # @api.onchange('internal_user')
    # def _onchange_internal_user(self):
    #     if self.internal_user:
    #         self.share = False
    #     else:
    #         self.share = True

    def write(self, values):
        res = super(ResUsers, self).write(values)

        # suppression du group "Employee" si l'utilisateur le possède
        try:
            self.env.cr.execute(
                "SELECT id FROM res_groups WHERE name = %s", ["Employee"]
            )
            group_employee_id = self.env.cr.fetchone()[0]

            if self.partner_id:
                if self.partner_id.customer:
                    self._cr.execute(
                        """DELETE FROM res_groups_users_rel WHERE uid=%s AND gid=%s""",
                        (self.id, group_employee_id),
                    )
        except:
            res = False

        # ajout du group Equipment Manager (pour qu'un client puisse ajouter ses équipements
        # self.env.cr.execute("SELECT id FROM res_groups WHERE name = %s", ['Equipment Manager'])
        # group_equipment_manager_id = self.env.cr.fetchone()[0]
        #
        # self._cr.execute("""SELECT 1 FROM res_groups_users_rel WHERE uid=%s AND gid=%s""",
        #                  (self.id, group_equipment_manager_id))
        # row = self._cr.fetchone()
        # if not row:
        #     self._cr.execute("""INSERT INTO res_groups_users_rel (gid,uid) VALUES (%s, %s)""",
        #                      (group_equipment_manager_id, self.id))

        return res

    @api.model_create_multi
    def create(self, values):
        users = super(ResUsers, self).create(values)
        for user in users:
            user.partner_id.write(
                {"company_id": user.company_id.id, "active": user.active}
            )

            # self.env.cr.execute("SELECT id FROM res_groups WHERE name = %s", ['Equipment Manager'])
        #    self.env.cr.execute("SELECT id FROM res_groups WHERE name = %s", ['Certification Manager'])
        #    group_equipment_manager_id = self.env.cr.fetchone()[0]

        # self._cr.execute(
        #    """INSERT INTO critt_equipment (name,category_id,owner_user_id,orga_certif,statut,of_cap_levage,periode) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        #    ('new equip if group equipment manager exist', 1, user.id, 'ok', 'Cap Levage', True, 0))

        # suppression du group "Employee" si l'utilisateur le possède
        # self.env.cr.execute("SELECT id FROM res_groups WHERE name = %s", ['Employee'])
        # group_employee_id = self.env.cr.fetchone()[0]
        # if user.partner_id.customer:
        #     self._cr.execute("""DELETE FROM res_groups_users_rel WHERE uid=%s AND gid=%s""",
        #                      (user.id, group_employee_id))

        # suppression du group "User: Own Documents Only" si l'utilisateur le possède
        # groupUserOwnDocs = self.env['res.groups'].search([('name', '=', 'User: Own Documents Only')])
        # if groupUserOwnDocs:
        #    self._cr.execute("""DELETE FROM res_groups_users_rel WHERE uid=? AND gid=?""",
        #                     (user.id, groupUserOwnDocs.id))
        # suppression du group "User: All Documents" si l'utilisateur le possède
        # groupUserAllDocuments = self.env['res.groups'].search([('name', '=', 'User: All Documents')])
        # if groupUserAllDocuments:
        #    self._cr.execute("""DELETE FROM res_groups_users_rel WHERE uid=? AND gid=?""",
        #                     (user.id, groupUserAllDocuments.id))

        # # ajout du group Equipment Manager (pour qu'un client puisse ajouter ses équipements
        # self._cr.execute("""SELECT 1 FROM res_groups_users_rel WHERE uid=%s AND gid=%s""",
        #                  (user.id, group_equipment_manager_id))
        # row = self._cr.fetchone()
        # if not row:
        #     self._cr.execute("""INSERT INTO res_groups_users_rel (gid,uid) VALUES (%s, %s)""",
        #                      (group_equipment_manager_id, user.id))

        # ajout du group Equipment Manager (pour qu'un client puisse ajouter ses équipements
        #    self._cr.execute("""SELECT 1 FROM res_groups_users_rel WHERE uid=2 AND gid=%s""", group_equipment_manager_id)
        #    row = self._cr.fetchone()
        #    if not row:
        #        self._cr.execute("""INSERT INTO res_groups_users_rel (gid,uid) VALUES (%s, 2)""", group_equipment_manager_id)

        # self._cr.execute("""SELECT 1 FROM res_groups_users_rel WHERE uid=%s AND gid=%s""",
        #                 (user.id, 1))
        # row = self._cr.fetchone()
        # if not row:
        #    self._cr.execute("""INSERT INTO res_groups_users_rel (gid,uid) VALUES (%s, %s)""", (1, user.id))

        # Si le droit sur le model critt_certification_audit pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute("SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.audit' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         #self._cr.execute(
        #        #     """INSERT INTO critt_equipment (name,category_id,owner_user_id,statut,orga_certif,of_cap_levage,periode) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        #          #   ('new equip pas de ir model access pour audit', 1, user.id, 'ok', 'Cap Levage', True, 0))
        #         model = self.env['ir.model'].sudo().search([('model', '=', 'critt.certification.audit')])
        #         #if model:
        #         #    self._cr.execute(
        #         #        """INSERT INTO critt_equipment (name,category_id,owner_user_id,statut,orga_certif,of_cap_levage,periode) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        #          #       ('new equip pas de ir model access pour audit: model ok', 1, user.id, 'ok', 'Cap Levage', True, 0))
        #         if model:
        #             #self._cr.execute(
        #             #    """INSERT INTO critt_equipment (name,category_id,owner_user_id,statut,orga_certif,of_cap_levage,periode) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        #             #    ('new equip model et group trouvés', 1, user.id, 'ok', 'Cap Levage', True, 0))
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", ('critt certification audit', True, model.id, group_equipment_manager_id, True, True, True, True, 1, now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                         now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.sale.order.line.equipment pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.sale.order.line.equipment' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.sale.order.line.equipment')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
        #             'critt.sale.order.line.equipment', True, model.id, group_equipment_manager_id, True, True, True, True, 1,
        #             now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #             now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model account.move pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     model = self.env['ir.model'].search([('model', '=', 'account.move')])
        #     if model:
        #         self._cr.execute(
        #             "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='account.move' AND ma.group_id=" + str(
        #                 group_equipment_manager_id))
        #         row = self._cr.fetchone()
        #         if not row:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                     write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'account.move for equipment manager', True, model.id,
        #                                  group_equipment_manager_id, True, True, True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model account.tax pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     model = self.env['ir.model'].search([('model', '=', 'account.tax')])
        #     if model:
        #         self._cr.execute(
        #             "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='account.tax' AND ma.group_id=" + str(
        #                 group_equipment_manager_id))
        #         row = self._cr.fetchone()
        #         if not row:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
        #                 'account.tax for equipment manager', True, model.id, group_equipment_manager_id, True, True, True,
        #                 True, 1,
        #                 now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                 now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #
        #     # Si le droit sur le model account.move.tax pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     model = self.env['ir.model'].search([('model', '=', 'account.move.tax')])
        #     if model:
        #         self._cr.execute(
        #             "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='account.move.tax' AND ma.group_id=" + str(
        #                 group_equipment_manager_id))
        #         row = self._cr.fetchone()
        #         if not row:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
        #                 'account.move.tax for equipment manager', True, model.id, group_equipment_manager_id, True, True, True,
        #                 True, 1,
        #                 now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                 now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model account.tax.group pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     model = self.env['ir.model'].search([('model', '=', 'account.tax.group')])
        #     if model:
        #         self._cr.execute(
        #             "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='account.tax.group' AND ma.group_id=" + str(
        #                 group_equipment_manager_id))
        #         row = self._cr.fetchone()
        #         if not row:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'account.tax.group for equipment manager', True, model.id, group_equipment_manager_id,
        #                                  True, True, True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.equipment')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment', True, model.id, group_equipment_manager_id, True, True, True, True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment.category pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment.category' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.equipment.category')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment.category', True, model.id, group_equipment_manager_id, True, True, True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment.organisme pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment.organisme' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.equipment.organisme')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                     write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment.organisme', True, model.id, group_equipment_manager_id,
        #                                  True, True, True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment.equipe pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment.equipe' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.equipment.equipe')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment.equipe', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True, True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment.agence pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment.agence' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.equipment.agence')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                             write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment.agence', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True, True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.questionnaire pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.questionnaire' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.certification.questionnaire')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.questionnaire', True, model.id, group_equipment_manager_id, True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.auditeur pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.auditeur' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.certification.auditeur')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.auditeur', True, model.id, group_equipment_manager_id, True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.ligne_saisie_utilisateur pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.ligne_saisie_utilisateur' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search([('model', '=', 'critt.certification.ligne_saisie_utilisateur')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.ligne_saisie_utilisateur', True, model.id, group_equipment_manager_id, True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.question pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.question' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.certification.question')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.question', True, model.id, group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.regroupement pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.regroupement' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.certification.regroupement')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.regroupement', True, model.id, group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.saisie_utilisateur pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.saisie_utilisateur' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.certification.saisie_utilisateur')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.saisie_utilisateur', True, model.id, group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.certificat pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.certificat' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.certification.certificat')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.certificat', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model res.users pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     model = self.env['ir.model'].search([('model', '=', 'res.users')])
        #     if model:
        #         self._cr.execute("SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='res.users' AND ma.group_id=" + str(group_equipment_manager_id))
        #         row = self._cr.fetchone()
        #         if not row:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
        #                 'res.users for equipment manager', True, model.id, group_equipment_manager_id, True, True, True, True, 1,
        #                 now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                 now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model res.partner pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     model = self.env['ir.model'].search([('model', '=', 'res.partner')])
        #     if model:
        #         self._cr.execute("SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='res.partner' AND ma.group_id=" + str(group_equipment_manager_id))
        #         row = self._cr.fetchone()
        #         if not row:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
        #                 'res.partner for equipment manager', True, model.id, group_equipment_manager_id, True, True,
        #                 True, True, 1,
        #                 now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                 now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.cout_audit pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     # self._cr.execute("SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.cout_audit' AND ma.group_id=" + str(group_equipment_manager_id))
        #     # row = self._cr.fetchone()
        #     # if not row:
        #     #     model = self.env['ir.model'].search(
        #     #         [('model', '=', 'critt.certification.cout_audit')])
        #     #     if model:
        #     #         now = datetime.now()
        #     #         self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #     #                                     write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #     #                          (
        #     #                              'critt.certification.cout_audit', True, model.id,
        #     #                              group_equipment_manager_id,
        #     #                              True, True,
        #     #                              True,
        #     #                              True, 1,
        #     #                              now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #     #                              now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model sale.order pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute("SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='sale.order' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'sale.order')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'sale.order', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model account.move pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute("SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='account.move' AND ma.group_id=" + str(group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'account.move')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'account.move', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.rapport_controle pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.rapport_controle' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.certification.rapport_controle')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.rapport_controle', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model ir.attachment pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='ir.attachment' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'ir.attachment')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                     write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'ir.attachment for critt certification', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model res.company pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='res.company' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'res.company')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'res.company for critt certification', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model product.product pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='product.product' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'product.product')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                                     write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'product.product for critt certification', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.certification.planification pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.certification.planification' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.certification.planification')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.certification.planification for critt certification', True, model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment.fabricant pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment.fabricant' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.equipment.fabricant')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                                             write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment.fabricant for critt certification', True,
        #                                  model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment.create_right pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment.create_right' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.equipment.create_right')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment.create_right', True,
        #                                  model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.horodating pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.horodating' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.horodating')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                                                     write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.horodating', True,
        #                                  model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment.equipe pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment.equipe' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.equipment.equipe')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                                                 write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment.equipe', True,
        #                                  model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        #     # Si le droit sur le model critt.equipment.agence pour le group 'Equipment Manager' n'existe pas, on l'ajoute
        #     self._cr.execute(
        #         "SELECT 1 FROM ir_model_access as ma JOIN ir_model as m ON m.id = ma.model_id WHERE m.model='critt.equipment.agence' AND ma.group_id=" + str(
        #             group_equipment_manager_id))
        #     row = self._cr.fetchone()
        #     if not row:
        #         model = self.env['ir.model'].search(
        #             [('model', '=', 'critt.equipment.agence')])
        #         if model:
        #             now = datetime.now()
        #             self._cr.execute("""INSERT INTO ir_model_access (name, active, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink, create_uid, create_date,
        #                                                                                         write_uid, write_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #                              (
        #                                  'critt.equipment.agence', True,
        #                                  model.id,
        #                                  group_equipment_manager_id,
        #                                  True, True,
        #                                  True,
        #                                  True, 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S"), 1,
        #                                  now.strftime("%Y-%m-%d %H:%M:%S")))
        #
        partner = self.env["res.partner"].search([("id", "=", users.partner_id.id)])

        partner.has_account = True

        return users
