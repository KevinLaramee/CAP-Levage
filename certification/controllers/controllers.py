# -*- coding: utf-8 -*-

import logging
from odoo import http
from odoo.http import request
import base64
from io import BytesIO

_logger = logging.getLogger(__name__)


class Audit(http.Controller):
    @http.route(
        [
            '/audit/completer_questionnaire/<model("critt.certification.audit"):audit>/<int:id_client>'
        ],
        type="http",
        auth="user",
        website=True,
    )
    def completer_questionnaire(self, audit, id_client, **post):
        Questionnaire = request.env["critt.certification.questionnaire"]
        SaisieUtilisateur = request.env["critt.certification.saisie_utilisateur"]
        Client = request.env["res.partner"]

        client = Client.sudo().search([("id", "=", id_client)], limit=1)
        saisie_utilisateur = SaisieUtilisateur.sudo().search(
            [("id_audit", "=", audit.id)], limit=1
        )
        if client and not saisie_utilisateur:
            vals = {
                "id_audit": audit.id,
                "id_questionnaire": audit.questionnaire.id,
                "id_client": id_client,
            }
            saisie_utilisateur = SaisieUtilisateur.create(vals)
        else:
            if not client:
                return request.render("website.403")

        if saisie_utilisateur.etat == "nouveau":
            regroupement, regroupement_nr, last = Questionnaire.regroupement_suivant(
                saisie_utilisateur, 0
            )
            donnees = {
                "audit": audit,
                "regroupement": regroupement,
                "regroupement_nr": regroupement_nr,
                "id_client": id_client,
            }
            if last:
                donnees.update({"last": True})
            return request.render("certification.questionnaire", donnees)
        # elif saisie_utilisateur.etat == "termine":
        #     return request.render('certification.questionnaire_termine', {'audit': audit,
        #                                                                'saisie_utilisateur': saisie_utilisateur,
        #                                                                'id_client': id_client})
        elif saisie_utilisateur.etat == "passe":
            regroupement, regroupement_nr, last = Questionnaire.regroupement_suivant(
                saisie_utilisateur,
                saisie_utilisateur.id_dernier_regroupement_affiche.id,
            )

            if not regroupement:
                (
                    regroupement,
                    regroupement_nr,
                    last,
                ) = Questionnaire.regroupement_suivant(
                    saisie_utilisateur,
                    saisie_utilisateur.id_dernier_regroupement_affiche.id,
                )

            donnees = {
                "audit": audit,
                "regroupement": regroupement,
                "regroupement_nr": regroupement_nr,
                "id_client": id_client,
            }
            if last:
                donnees.update({"last": True})
            return request.render("certification.questionnaire", donnees)

        else:
            return request.render("website.403")

    @http.route(
        [
            '/audit/soumettre_reponses/<model("critt.certification.audit"):audit>/<int:id_client>'
        ],
        type="http",
        auth="user",
        website=True,
    )
    def soumettre(self, audit, id_client, **post):
        Certificat = request.env["critt.certification.certificat"]
        Rapport_vgp = request.env["critt.certification.rapport_controle"]
        _logger.debug("Données entrantes: %s", post)
        id_regroupement = int(post["id_regroupement"])
        questions = request.env["critt.certification.question"].search(
            [("id_regroupement", "=", id_regroupement)]
        )

        # erreurs = {}
        for question in questions:
            tag_reponse = "%s_%s_%s" % (
                audit.questionnaire.id,
                id_regroupement,
                question.id,
            )
            # erreurs.update(question.validation_question(post, tag_reponse))

        # ret = {}
        # if len(erreurs):
        #     ret['erreurs'] = erreurs
        # else:
        try:
            saisie_utilisateur = (
                request.env["critt.certification.saisie_utilisateur"]
                .sudo()
                .search([("id_audit", "=", audit.id)], limit=1)
            )
        except KeyError:
            return request.render("website.403")
        id_utilisateur = request.env.user

        for question in questions:
            tag_reponse = "%s_%s_%s" % (
                audit.questionnaire.id,
                id_regroupement,
                question.id,
            )
            request.env["critt.certification.ligne_saisie_utilisateur"].with_user(
                id_utilisateur
            ).sauv_ligne(saisie_utilisateur.id, question, post, tag_reponse)

        regroupement_suivant, _, derniere = request.env[
            "critt.certification.questionnaire"
        ].regroupement_suivant(saisie_utilisateur, id_regroupement)
        vals = {"id_dernier_regroupement_affiche": id_regroupement}
        if regroupement_suivant is None:
            audit.update({"etat_audit": "termine"})
            vals.update({"etat": "termine"})

            equipement = (
                request.env["critt.equipment"]
                .sudo()
                .search([("id", "=", audit.equipement.id)], limit=1)
            )

            equipement.update(
                {
                    "audit_suivant": audit.date_suivant,
                    "last_general_observation": post["observ_gene"],
                }
            )

            vals = {
                "list_equipment": audit.equipement.id,
                "client": id_client,
                "list_audits": audit.id,
            }

            rapport_controle = Rapport_vgp.create(vals)

            rapport_controle.update(
                {
                    "number": "VGP" + str(rapport_controle.id),
                    "url": "/report/pdf/certification.report_controle_template/%s"
                    % str(rapport_controle.id),
                }
            )

            if post.get("button_submit_valide"):
                audit.update({"acces_certif": True})
                equipement.update({"statut": "ok"})
                audit.update({"etat_equipment_fin": "Certifié"})
                # Création lien certif vue equipements
                # Remplissage du champ pdf
                pdf = "/report/pdf/certification.report_certificat_conforme/" + str(
                    audit.id
                )

                # Remplissage du champ desc
                desc = "Contrôle du " + audit.date.strftime("%d/%m/%Y")

                vals2 = {
                    "desc": desc,
                    "date": audit.date,
                    "pdf": pdf,
                    "id_audit": audit.id,
                    "id_equipment": audit.equipement.id,
                    "type": "controle",
                    "sequence": 2,
                }

                Certificat.create(vals2)
                audit.update({"certif_conforme": True})

                return request.redirect(
                    "/web#id=%s&view_type=form&model=critt.equipment&action=certification.act_equipement_view"
                    % equipement.id
                )

            if post.get("button_submit_reparation"):
                Horodating = request.env["critt.horodating"]
                vals = {
                    "user": request.env.user.id,
                    "action": "Blocage matériel",
                    "equipment_id": equipement.id,
                }
                Horodating.create(vals)
                equipement.update({"statut": "bloque"})
                audit.update({"etat_equipment_fin": "Réparation(s) à faire"})
                devis = equipement.action_creer_devis()
                return request.redirect(
                    "/web#id=%s&view_type=form&model=sale.order&action=certification.act_order_view"
                    % devis
                )

            if post.get("button_submit_reforme"):
                audit.update({"acces_certif": True})
                equipement.update({"statut": "reforme", "audit_suivant": None})
                audit.update({"etat_equipment_fin": "Réformé"})

                return request.redirect(
                    "/web#id=%s&view_type=form&model=critt.equipment&action=certification.act_equipement_view"
                    % equipement.id
                )

        else:
            vals.update({"etat": "passe"})
            audit.update({"etat_audit": "debute"})

        saisie_utilisateur.with_user(id_utilisateur).write(vals)

        return request.redirect(
            "/audit/completer_questionnaire/%s/%s" % (audit.id, id_client)
        )

    @http.route(
        [
            '/audit/reponses_questionnaire/<model("critt.certification.audit"):audit>/<int:id_client>/<int:num_regroupement>'
        ],
        type="http",
        auth="user",
        website=True,
    )
    def reponses_questionnaire(self, audit, id_client, num_regroupement, **post):
        id_regroupements = []
        for regroupement in audit.questionnaire.ids_regroupement:
            id_regroupements.append(int(regroupement.id))

        id_regroupement_affiche = id_regroupements[num_regroupement]
        regroupement_affiche = request.env["critt.certification.regroupement"].search(
            [("id", "=", id_regroupement_affiche)]
        )
        ids_questions_regroupement_affiche = request.env[
            "critt.certification.question"
        ].search([("id_regroupement", "=", id_regroupement_affiche)])

        reponses = request.env["critt.certification.saisie_utilisateur"].search(
            [("id_client", "=", id_client), ("id_audit", "=", audit.id)]
        )
        lignes_reponses = []
        for id_question in ids_questions_regroupement_affiche:
            ligne_reponse = request.env[
                "critt.certification.ligne_saisie_utilisateur"
            ].search(
                [
                    ("id_saisie_utilisateur", "=", reponses.id),
                    ("id_question", "=", id_question.id),
                ]
            )
            lignes_reponses.append(ligne_reponse)

        if len(id_regroupements) == 1:
            regroupement_suivant = None
            regroupement_precedent = None
        else:
            if len(id_regroupements) > 1:
                if num_regroupement == 0:
                    regroupement_suivant = num_regroupement + 1
                    regroupement_precedent = None
                else:
                    if num_regroupement == (len(id_regroupements) - 1):
                        regroupement_suivant = None
                        regroupement_precedent = num_regroupement - 1
                    else:
                        regroupement_suivant = num_regroupement + 1
                        regroupement_precedent = num_regroupement - 1

        return request.render(
            "certification.reponses_questionnaire",
            {
                "audit": audit,
                "lignes_reponses": lignes_reponses,
                "id_client": id_client,
                "regroupement_nr": 0,
                "regroupement_affiche": regroupement_affiche,
                "regroupement_suivant": regroupement_suivant,
                "regroupement_precedent": regroupement_precedent,
                "num_regroupement": num_regroupement,
            },
        )


class ResUsers(http.Controller):
    @http.route(
        ["/reinitialiser_mdp/<int:id>"], type="http", auth="public", website=True
    )
    def reinit_mdp(self, id, **post):
        user = request.env["res.users"].search([("id", "=", id)])

        user.action_reset_password()

        return "{'success': 'true'}"


class Equipment(http.Controller):
    @http.route(["/testsavephoto"], type="http", auth="user", website=True, csrf=False)
    def testsavephoto(self, **post):
        equipment_id = post.get("equipment_id")
        equip = request.env["critt.equipment"].browse(int(equipment_id))

        if post.get("data"):
            # equip.image = post['data']
            self._set_equipment_image(request, post.get("data"), equip)
            # super(Equipment, self).write(equip)
            # template = {
            #     'name': 'image',
            #     'res_name': equipment.name,
            #     'res_model': 'critt.equipment',
            #     'res_field': 'image',
            #     'res_id': equipment.id,
            #     'type': 'binary',
            #     'datas_fname': file.filename,  # 'image small.png',
            #     'datas': post['data'],
            #     'checksum': ''
            # }
        # template = {
        #    'localisation_description': 'test2'
        # }
        # equip.write(template)

    def _set_equipment_image(self, request, data, equipment):
        # remove ir.attachement image
        request.env.cr.execute(
            "SELECT DISTINCT id FROM ir_attachment WHERE name IN ('image', 'image_medium', 'image_small') AND res_model = 'critt.equipment' AND res_id = %s",
            (equipment.id,),
        )
        attachement_ids = [x[0] for x in request.env.cr.fetchall()]
        for attachement_id in attachement_ids:
            attachmentToDelete = request.env["ir.attachment"].browse(
                int(attachement_id)
            )
            attachmentToDelete.sudo().unlink()

        Attachments = request.env["ir.attachment"]

        template = {
            "name": "image",
            "res_name": equipment.name,
            "res_model": "critt.equipment",
            "res_field": "image",
            "res_id": equipment.id,
            "type": "binary",
            "datas_fname": "photo.png",  # 'image small.png',
            "datas": data,
            "checksum": "",
        }
        attachment_image_id = Attachments.sudo().create(template)
        template = {
            "name": "image_medium",
            "res_name": equipment.name,
            "res_model": "critt.equipment",
            "res_field": "image_medium",
            "res_id": equipment.id,
            "type": "binary",
            "datas_fname": "photo.png",  # 'image small.png',
            "datas": data,
            "checksum": "",
        }
        attachment__image_medium_id = Attachments.sudo().create(template)
        template = {
            "name": "image_small",
            "res_name": equipment.name,
            "res_model": "critt.equipment",
            "res_field": "image_small",
            "res_id": equipment.id,
            "type": "binary",
            "datas_fname": "photo.png",  # 'image small.png',
            "datas": data,
            "checksum": "",
        }
        attachment__image_medium_id = Attachments.sudo().create(template)
