# import math
#
# from werkzeug import urls
#
# from odoo import fields as odoo_fields, tools, _
# from odoo.osv import expression
# from odoo.exceptions import ValidationError
# from odoo import http
# from odoo.http import Controller, request, route
# from odoo.addons.web.controllers.main import WebClient
# from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
# import time, datetime
# from collections import OrderedDict
# from odoo.osv.expression import OR
# from odoo.tools.config import config
# from datetime import date, timedelta
# from PIL import Image
# import calendar
#
# from werkzeug.urls import url_encode
#
# import numbers
# import requests
# import os
# import ssl
# import shutil
# import tempfile
# import urllib.request
#
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# import json
#
# from odoo import api
# from odoo.tools import pycompat
# import base64
#
#
# from random import *
#
# class website(Controller):
#
#
#
#
# 	#pour télécharger un fichier
# 	#@http.route('/my/test', type='http', methods=['GET'], auth="public")
# 	#def get_test(self, **kwargs):
# 		#url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
# 		#myfile = requests.get(url)
# 		#open('d:test.zip', 'wb').write(myfile.content)
#
# 	_items_per_page = 10
#
# 	def _prepare_portal_layout_values_home(self):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				#values = super(main, self)._prepare_portal_layout_values()
# 				values = { 'quotation_count': 0, 'order_count': 0, 'order_count2': 0, 'equipments_count': 0}
# 				partner = request.env.user.partner_id
#
# 				SaleOrder = request.env['sale.order']
# 				quotation_count = SaleOrder.search_count([
# 					('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
# 					('state', 'in', ['sent', 'cancel'])
# 				])
# 				order_count = SaleOrder.search_count([
# 					('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
# 					('state', 'in', ['sale', 'done'])
# 				])
# 				order_count2 = SaleOrder.search_count([
# 					('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
# 					('state', 'in', ['sale', 'done'])
# 				])
# 				purchases_count = SaleOrder.search_count([('state', 'in', ['draft'])])
#
# 				Equipment = request.env['critt.equipment']
# 				equipments_count = Equipment.search_count([('active', '=', True), ('owner_user_id', '=', request.env.user.id)])
#
# 				SaleOrder = request.env['sale.order']
# 				requests_count = SaleOrder.search_count([('state', 'in', ['draft', 'sent']), ('partner_id', '=', request.env.user.partner_id.id)])
#
# 				values.update({
# 					'quotation_count': quotation_count,
# 					'order_count': order_count,
# 					'order_count2': order_count2,
# 					'purchases_count': purchases_count,
# 					'equipments_count': equipments_count,
# 					'requests_count': requests_count
# 				})
# 				return values
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	def _prepare_portal_layout_values_equipments(self):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				values = { 'equipments_count': 0}
#
# 				Equipment = request.env['critt.equipment']
# 				equipments_count = Equipment.search_count([('active', '=', True), ('owner_user_id', '=', request.env.user.id)])
#
# 				values.update({
# 					'equipments_count': equipments_count
# 				})
#
# 				return values
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	def _prepare_portal_layout_values_equipments(self):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				values = {'equipments_count': 0}
#
# 				Equipment = request.env['critt.equipment']
# 				equipments_count = Equipment.search_count([('active', '=', True), ('owner_user_id', '=', request.env.user.id)])
#
# 				values.update({
# 					'equipments_count': equipments_count
# 				})
#
# 				return values
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	def _prepare_portal_layout_values_requests(self):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				values = { 'requests_count': 0}
#
# 				SaleOrder = request.env['sale.order']
# 				requests_count = SaleOrder.sudo().search_count([('state', 'in', ['draft', 'sent']), ('partner_id', '=', request.env.user.partner_id.id)])
#
# 				values.update({
# 					'requests_count': requests_count
# 				})
#
# 				return values
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@route(['/'], type='http', auth="public", website=True)
# 	def acceuil(self):
# 		#if request.env.user.gest_materiel == False:
# 		#	return request.render("website.homepage")
# 		#return request.render("website.homepage")
# 		if request.env.user.has_group('base.group_portal') or request.env.user.has_group('base.group_user'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 					# return request.redirect('/my/equipments')
# 					return request.redirect('/my/equipments/tracking')
# 				else:
# 					return request.render("website.homepage")
# 		else:
# 			#return request.redirect('/my/identification?origin=bo')
# 			# return request.redirect('/web#action=certification.act_equipement_view&model=critt.equipment&view_type=list')
# 			# values = self._prepare_portal_layout_values_home()
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@route(['/certification/home'], type='http', auth="user", website=True)
# 	def home(self, fw='', **kw):
# 		#return request.redirect('/my/certification/home?fw=5')
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				if request.env.user.has_group('base.group_portal'):
# 					# return request.redirect('/my/equipments')
# 					return request.redirect('/my/equipments/tracking')
# 				else:
# 					if request.env.user.has_group('certification.certification_lvl_3'):
# 						#return request.redirect('/my/identification?origin=bo')
# 						return request.redirect('/web#home')
# 						#return request.redirect('/web#action=certification.act_equipement_view&model=critt.equipment&view_type=list')
# 					else:
# 						return request.redirect('/web#home')
#
# 				values = self._prepare_portal_layout_values_home()
# 				return request.render("portal.portal_my_home", values)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route('/my/token', type='http', methods=['GET'], auth="public")
# 	def get_token(self, **kwargs):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group(
# 				'certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				return json.dumps({'token': request.csrf_token()})
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("subscribe.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route('/updateagenceequipe', type='http', methods=['GET'], auth="public")
# 	def updateagenceequipe(self, **kwargs):
# 		# equipments = request.env['critt.equipment'].search([('res_partner_id', '=', 60)], order='num_materiel asc')
# 		equipments = request.env['critt.equipment'].search([], order='num_materiel asc')
# 		for equipment in equipments:
# 			if equipment.agence_id:
# 				if equipment.agence_id.id != equipment.res_partner_id.id:
# 					agence = request.env['res.partner'].sudo().search([('id', '=', equipment.agence_id.id)], limit=1)
# 					if agence:
# 						agence = agence.sudo().sudo().write({
# 							'parent_id': equipment.res_partner_id.id
# 						})
# 			if equipment.equipe_id:
# 				if equipment.equipe_id.id != equipment.res_partner_id.id:
# 					equipe = request.env['res.partner'].sudo().search([('id', '=', equipment.equipe_id.id)], limit=1)
# 					if equipe:
# 						equipe = equipe.sudo().sudo().write({
# 							'parent_id': equipment.res_partner_id.id
# 						})
#
# 		return json.dumps({'ok': 'oui'})
#
# 	@http.route('/my/get_datas_certificat', type='http', methods=['GET'], auth="public")
# 	def get_datas_certificat(self, id='', type='', **kwargs):
# 		#if request.env.user.has_group('certification.website_lvl_1'):
# 		path = ''
# 		filename = ''
# 		error = ''
#
# 		certificat = None
# 		if type == 'creation':
# 			certificat = request.env['critt.certification.certificat'].sudo().search(
# 				[('type', '=', 'creation'), ('id_equipment', '=', int(id))])
# 		elif type == 'destruction':
# 			certificat = request.env['critt.certification.certificat'].sudo().search(
# 				[('type', '=', 'reforme'), ('id_equipment', '=', int(id))])
# 		else:
# 			certificat = request.env['critt.certification.certificat'].sudo().search(
# 				[('type', '=', 'controle'), ('id_audit', '=', int(id))])
# 			audit = request.env['critt.certification.audit'].sudo().search([('id', '=', int(id))])
# 			if audit:
# 				if audit.acces_certif == False:
# 					error = str(1)  # 'Le certificat n\'est pas encore disponible'
#
# 		if len(error) == 0:
# 			if certificat:
# 				ir_act_report_xml = request.env['ir.actions.report']
# 				# report_certificat_destruction
# 				if type == 'creation':
# 					report_xml = ir_act_report_xml.sudo().search(
# 						[('report_name', '=', 'certification.report_certificat_creation')])
# 				elif type == 'destruction':
# 					report_xml = ir_act_report_xml.sudo().search(
# 						[('report_name', '=', 'certification.report_certificat_destruction')])
# 				else:
# 					report_xml = ir_act_report_xml.sudo().search(
# 						[('report_name', '=', 'certification.report_certificat_conforme')])
#
# 				if report_xml:
# 					pdf = report_xml[0].sudo().render_qweb_pdf(int(id))[0]
#
# 					# attachment = request.env['ir.attachment'].sudo().search([('res_model', '=', 'critt.certification.audit'), ('res_id', '=', int(id)), ('res_model', '=', 'certificat_conforme.pdf')])
# 					# template = {
# 					#	'name': 'certificat_conforme.pdf',
# 					#	'res_field': '',
# 					#	'datas_fname': 'certificat_conforme.pdf',  # 'image small.png',
# 					#	'res_name': 'certificat_conforme.pdf',
# 					#	'type': 'binary',
# 					#	'res_model': 'critt.certification.audit',
# 					#	'res_id': id,
# 					#	'datas': base64.encodestring(pdf),
# 					#	'checksum': '',
# 					#	'description': ''
# 					# }
# 					# Attachments = request.env['ir.attachment']
# 					# if attachment:
# 					#	attachment.write(template)
# 					# else:
# 					#	attachment = Attachments.sudo().create(template)
#
# 					return base64.encodestring(pdf)
# 				else:
# 					error = str(3)  # 'Aucun certificat trouvé'
# 			else:
# 				error = str(4)  # 'Aucun certificat trouvé'
#
#
#
#
# 		return error
# 		#else:
# 			#return request.render("website.homepage")
#
# 	#EQUIPMENTS
# 	#send message
# 	@http.route(['/my/', '/my/send/message'], type='http', auth="user", website=True)
# 	def portal_send_message(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				server = smtplib.SMTP()  # Avec TLS, on utilise SMTP()
# 				# server.set_debuglevel(1) # Décommenter pour activer le debug
# 				server.connect('smtp.gmail.com', 587)  # On indique le port TLS
# 				# (220, 'toto ESMTP Postfix') # Réponse du serveur
# 				server.ehlo()  # On utilise la commande EHLO
# 				# (250, 'toto\nPIPELINING\nSIZE 10240000\nVRFY\nETRN\nSTARTTLS\nENHANCEDSTATUSCODES\n8BITMIME\nDSN') # Réponse du serveur
# 				server.starttls()  # On appelle la fonction STARTTLS
# 				# (220, '2.0.0 Ready to start TLS') # Réponse du serveur
# 				server.login('caplevage.test@gmail.com', 'jZSX5NbtUIjwXe3piPLu7')
# 				# (235, '2.7.0 Authentication successful') # Réponse du serveur
# 				fromaddr = 'Cap Levage <caplevage.test@gmail.com>'
# 				toaddrs = ['caplevage.test@gmail.com']  # On peut mettre autant d'adresses que l'on souhaite
# 				sujet = "[Cap Levage][Message]: " + post['send_message_objet']
#
# 				html = u"""\
# 				<html>
# 				<head>
# 				<meta charset="utf-8" />
# 				</head>
# 				<body>
# 				<div>
# 					<br>Nom: """ + post['send_message_name'] + u"""\
# 					<br>Adresse mail: """ + post['send_message_mail'] + u"""\
# 					<br>Objet: """ + post['send_message_objet'] + u"""\
# 					<br>Message: """ + post['send_message_message'] + u"""\
# 				</div>
# 				</body
# 				</html>
# 				"""
#
# 				msg = MIMEMultipart('alternative')
# 				msg['Subject'] = sujet
# 				msg['From'] = fromaddr
# 				msg['To'] = ','.join(toaddrs)
#
# 				part = MIMEText(html, 'html')
# 				msg.attach(part)
# 				try:
# 					server.sendmail(fromaddr, toaddrs, msg.as_string())
# 				except smtplib.SMTPException as e:
# 					print(e)
# 				# {} # Réponse du serveur
# 				server.quit()
#
# 				return request.redirect(post['current_path'])
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	#planning
# 	@http.route(['/my/', '/my/planning'], type='http', auth="user", website=True)
# 	def portal_planning(self, origin='', **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
#
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM res_partner "
# 					"WHERE customer_rank = %s",
# 					(3,))
#
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				clients = request.env['res.partner'].sudo().browse(ids)
#
# 				now = datetime.datetime.now()
# 				request.env.cr.execute(
# 					"SELECT DISTINCT p.id"
# 					" FROM res_partner as c"
# 					" JOIN critt_certification_planification as p ON p.client = c.id"
# 					" WHERE p.date < %s",
# 					(now.strftime("%Y-%m-%d %H:%M:%S"),))
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				clientsWithPlanification = request.env['critt.certification.planification'].sudo().browse(ids)
#
# 				#request.env.cr.execute(
# 				#	"SELECT DISTINCT id FROM critt_equipment "
# 				#	"WHERE owner_user_id = %s",
# 				#	(request.env.user.id,))
#
# 				#ids = [x[0] for x in request.env.cr.fetchall()]
# 				#equipments_planifies = request.env['critt.equipment'].sudo().browse(ids)
#
#
# 				return request.render("certification.portal_planning", {
# 					'origin': origin,
# 					'clients': clients,
# 					#'equipmentsForPlanning': equipmentsForPlanning,
# 					'cleintsWithPlanification': clientsWithPlanification
# 				})
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route(['/my/planning/addorupdate'], type='http', auth="user", website=True)
# 	def portal_planning_addorupdate(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				res = False
#
# 				error = ''
# 				#num_materiel = post['num_materiel']
# 				client_id = post['client_id']
# 				planification_id = int(post['planification_id'])
# 				origin = post['origin']
#
# 				#etat_audit = ''
# 				#equipment_id = ''
# 				#title = ''
# 				#statut_materiel = ''
# 				#statut_materiel_libelle = ''
#
# 				#soustraire 2 heures, l'heure retourner par le calendrier est en avance
# 				try:
# 					#2019-08-07 04:30:00
# 					#d = datetime.datetime.strptime(post['start'], "%Y-%m-%d %H:%M:%S") - timedelta(hours=2)
# 					d = datetime.datetime.strptime(post['start'], "%Y-%m-%d %H:%M:%S") - timedelta(hours=1)
# 					start = d.strftime("%Y-%m-%d %H:%M:%S")
# 				except:
# 					end = post['end']
# 				try:
# 					#2019-08-07 04:30:00
# 					#d = datetime.datetime.strptime(post['end'], "%Y-%m-%d %H:%M:%S") - timedelta(hours=2)
# 					d = datetime.datetime.strptime(post['end'], "%Y-%m-%d %H:%M:%S") - timedelta(hours=1)
# 					end = d.strftime("%Y-%m-%d %H:%M:%S")
# 				except:
# 					end = post['end']
#
# 				client = request.env['res.partner'].sudo().search([('id', '=', client_id)])
# 				if client:
# 					template = {
# 						'client': client.id,
# 						'date': start,
# 						'fin': end
# 					}
# 					planification = request.env['critt.certification.planification']
# 					try:
# 						if planification_id == -1:
# 							planification = planification.sudo().create(template)
# 							res = True
# 							planification_id = planification.id
# 						else:
# 							planification = request.env['critt.certification.planification'].sudo().search([('id', '=', planification_id)])
# 							if planification:
# 								template = {
# 									'date': start,
# 									'fin': end
# 								}
# 								planification = planification.sudo().write(template)
# 							res = True
# 					except Exception as e:
# 						error = str(e)
# 						res = False
# 				else:
# 					error = 'Aucun client correspondant'
# 					res = False
#
# 				return json.dumps({
# 					'res': res, 'error': error,
# 					'planification_id': planification_id,
# 					'client_name': client.name
# 					#'num_materiel': num_materiel,
# 					#'etat_audit': etat_audit,
# 					#'equipment_id': equipment_id,
# 					#'statut_materiel': statut_materiel,
# 					#'statut_materiel_libelle': statut_materiel_libelle
# 				})
#
# 		# @http.route(['/my/', '/my/nfc_search'], type='http', auth="user", website=True)
# 		# def portal_nfc_search(self, search_nfc='', **kw):
# 		#
# 		# 	if len(search_nfc) > 0:
# 		# 		equipments = request.env['critt.equipment'].search(
# 		# 			[('nfc', '=', search_nfc)])
# 		# 		if len(equipments) == 1:
# 		# 			return request.redirect(
# 		# 				'/web#id=%s&view_type=form&model=critt.equipment&action=certification.act_equipement_view' % (
# 		# 					equipments[0].id))
# 		#
# 		# 	return request.redirect('/web#action=certification.act_equipement_view&model=critt.equipment&view_type=list')
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route(['/my/qr_code_search'], type='http', auth="user", website=True)
# 	def back_qr_code_search(self, search_qr_code='', **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				if len(search_qr_code) > 0:
# 					equipments = request.env['critt.equipment'].search(['|',('qr_code', '=', search_qr_code), ('num_materiel', '=', search_qr_code)])
# 					if len(equipments) == 1:
# 						Horodating = request.env['critt.horodating']
#
# 						vals = {'user': request.env.user.id, 'action': "Recherche QR Code", 'equipment_id': equipments[0].id}
#
# 						Horodating.create(vals)
#
# 						return request.redirect(
# 							'/web#id=%s&view_type=form&model=critt.equipment&action=certification.act_equipement_view' % (
# 								equipments[0].id))
#
# 				return request.redirect('/web#action=certification.act_equipement_view&model=critt.equipment&view_type=list')
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# Identification
# 	@http.route(['/my/', '/my/identification'], type='http', auth="user", website=True)
# 	def portal_identification_equipment(self, search='', origin='', **kw): #, search_nfc=''
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				if request.env.user.partner_id.gest_materiel == False:
# 					if origin == 'bo':
# 						return request.redirect('/web#action=certification.act_equipement_view')
# 					else:
# 						return request.redirect('/')
#
# 				# clf = nfc.ContactlessFrontend()
# 				# assert clf.open('usb:072f:2200') is True
# 				# clf.close()
#
# 				if origin == 'bo':
# 					request.env.cr.execute(
# 						"SELECT DISTINCT id FROM critt_equipment "
# 						"WHERE statut != 'reforme'",
# 						(request.env.user.id,))
# 				else:
# 					request.env.cr.execute(
# 						"SELECT DISTINCT id FROM critt_equipment "
# 						"WHERE owner_user_id = %s AND statut != 'reforme'",
# 						(request.env.user.id,))
#
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				equipmentsForPlanning = request.env['critt.equipment'].sudo().browse(ids)
#
# 				if origin == 'bo':
# 					request.env.cr.execute(
# 						"SELECT DISTINCT a.id"
# 						" FROM critt_equipment as e"
# 						" JOIN critt_certification_audit as a ON a.equipement = e.id"
# 						" WHERE a.etat_audit IN ('planifie') AND e.statut != 'reforme'",
# 						(request.env.user.id,))
# 				else:
# 					request.env.cr.execute(
# 						"SELECT DISTINCT a.id"
# 						" FROM critt_equipment as e"
# 						" JOIN critt_certification_audit as a ON a.equipement = e.id"
# 						" WHERE a.etat_audit IN ('planifie') AND e.owner_user_id = %s AND e.statut != 'reforme'",
# 						(request.env.user.id,))
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				equipmentsWithAudit = request.env['critt.certification.audit'].sudo().browse(ids)
#
# 				today = date.today()
# 				one_month_later = today + timedelta(days=+30)
# 				if origin == 'bo':
# 					controls_to_plan = request.env['critt.equipment'].search(
# 						[('audit_suivant', '>', today.strftime("%Y-%m-%d")),
# 						 ('audit_suivant', '<=', one_month_later.strftime("%Y-%m-%d"))])
# 					quotes = request.env['sale.order'].search(
# 						[('state', 'in', ['sale'])])
# 				else:
# 					controls_to_plan = request.env['critt.equipment'].search(
# 						[('audit_suivant', '>', today.strftime("%Y-%m-%d")),
# 						 ('audit_suivant', '<=', one_month_later.strftime("%Y-%m-%d")),
# 						 ('owner_user_id', '=', request.env.user.id)])
# 					quotes = request.env['sale.order'].search(
# 						[('partner_id', '=', request.env.user.partner_id.id), ('state', 'in', ['sent'])])
# 				next_controls = []
#
# 				# if len(search_nfc) > 0:
# 				# 	if origin == 'bo':
# 				# 		equipments = request.env['critt.equipment'].search(
# 				# 			[('nfc', '=', search_nfc)])
# 				# 	else:
# 				# 		equipments = request.env['critt.equipment'].search(
# 				# 			[('nfc', '=', search_nfc), ('owner_user_id', '=', request.env.user.id)])
# 				# 	if len(equipments) == 1:
# 				# 		if origin == 'bo':
# 				# 			return request.redirect(
# 				# 				'/web#id=%s&view_type=form&model=critt.equipment&action=certification.act_equipement_view' % (
# 				# 					equipments[0].id))
# 				# 		else:
# 				# 			return request.redirect('/my/equipment/%s' % (equipments[0].id))
# 				#
# 				# 	if len(equipments) == 0:
# 				# 		values = {
# 				# 			'equipment': False,
# 				# 			'search': search,
# 				# 			'search_nfc': search_nfc,
# 				# 			'controls_to_plan': controls_to_plan,
# 				# 			'next_controls': next_controls,
# 				# 			'quotes': quotes,
# 				# 			'origin': origin,
# 				# 			'equipmentsForPlanning': equipmentsForPlanning,
# 				# 			'equipmentsWithAudit': equipmentsWithAudit
# 				# 		}
# 				# 		return request.render("certification.portal_identification_equipment", values)
# 				# return request.redirect('/my/equipments/tracking')
#
# 				if len(search) == 0:
# 					values = {
# 						'equipment': False,
# 						'search': search,
# 						# 'search_nfc': search_nfc,
# 						'controls_to_plan': controls_to_plan,
# 						'next_controls': next_controls,
# 						'quotes': quotes,
# 						'origin': origin,
# 						'equipmentsForPlanning': equipmentsForPlanning,
# 						'equipmentsWithAudit': equipmentsWithAudit
# 					}
# 					return request.render("certification.portal_identification_equipment", values)
#
# 				if search == "*":
# 					search = ""
#
# 				if origin == 'bo':
# 					equipments = request.env['critt.equipment'].search(
# 						[('num_materiel', 'ilike', search)])
# 				else:
# 					equipments = request.env['critt.equipment'].search(
# 						[('num_materiel', 'ilike', search), ('owner_user_id', '=', request.env.user.id)])
#
# 				# Si un seul résultat, redirection vers la fiche du matériel (soit vers le backoffice, soit vers le front)
# 				if len(equipments) == 1:
# 					if origin == 'bo':
# 						return request.redirect(
# 							'/web#id=%s&view_type=form&model=critt.equipment&action=certification.act_equipement_view' % (
# 								equipments[0].id))
# 					else:
# 						return request.redirect('/my/equipment/%s' % (equipments[0].id))
#
# 				# si plusiseurs résultats, soit on redirige vers la page de résutlat du front office, soit on affiche la liste des matériels du backoffice
# 				if len(equipments) > 1:
# 					if origin == 'bo':
# 						return request.redirect(
# 							'/web#view_type=list&model=critt.equipment&action=certification.act_equipement_view&num_materiel=01')
# 					else:
# 						return request.redirect('/my/equipments?search_in=num_materiel&search=%s' % (search))
#
# 				values = {
# 					'equipment': False,
# 					'search': search,
# 					# 'search_nfc': search_nfc,
# 					'controls_to_plan': controls_to_plan,
# 					'next_controls': next_controls,
# 					'quotes': quotes,
# 					'origin': origin,
# 					'equipmentsForPlanning': equipmentsForPlanning,
# 					'equipmentsWithAudit': equipmentsWithAudit
# 				}
# 				return request.render("certification.portal_identification_equipment", values)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	#Suivi des matériels
# 	@http.route(['/my/equipments', '/my/equipments/tracking'], type='http', auth="user", website=True)
# 	def portal_my_tracking(self, date_start='', date_end='', **kw): #, search_nfc=''
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				#if request.env.user.gest_materiel == False:
# 				#	return request.redirect('/')
#
# 				# search_nfc_result = -1
# 				# if len(search_nfc) > 0:
# 				# 	search_nfc_result = 1
# 				# 	equipments = request.env['critt.equipment'].search(
# 				# 		[('nfc', '=', search_nfc), ('owner_user_id', '=', request.env.user.id)])
# 				# 	if len(equipments) == 1:
# 				# 		return request.redirect('/my/equipment/%s' % (equipments[0].id))
#
# 				partner = request.env.user.partner_id
# 				# audit_suivant date_dernier_audit
# 				request_search = ''
# 				if len(date_start) > 0 and len(date_end) > 0:
# 					request_search = " AND audit_suivant >= '" + date_start + "' and audit_suivant <= '" + date_end + "'"
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM critt_equipment "
# 					"WHERE owner_user_id = %s" + request_search,
# 					(request.env.user.id,))
#
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				equipments = request.env['critt.equipment'].sudo().browse(ids)
#
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM res_partner "
# 					"WHERE parent_id = %s",
# 					(partner.id,))
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				referents = request.env['res.partner'].sudo().browse(ids)
#
# 				#equipes = request.env['critt.equipment.equipe'].search([('owner_user_id', '=', request.env.user.id)])
# 				#agences = request.env['critt.equipment.agence'].search([('owner_user_id', '=', request.env.user.id)])
#
# 				equipes = request.env['res.partner'].sudo().search([
# 					('parent_id', '=', request.env.user.partner_id.id), ('type', '=', 'contact')
# 				])
# 				agences = request.env['res.partner'].sudo().search([
# 					('parent_id', '=', request.env.user.partner_id.id), ('type', '=', 'delivery')
# 				])
#
# 				return request.render("certification.portal_my_equipments_tracking",
# 									  {
# 										  'user': request.env.user,
# 										  'partner': partner,
# 										  'referents': referents,
# 										  'equipes': equipes,
# 										  'agences': agences,
# 										  'equipments': equipments,
# 										  'date_start': date_start,
# 										  'date_end': date_end,
# 										  # 'search_nfc': search_nfc,
# 										  # 'search_nfc_result': search_nfc_result
# 									  })
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route(['/my/reports'], type='http', auth="user", website=True)
# 	def my_reports_view(self):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				return request.render("certification.my_reports", {'user': request.env.user})
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route(['/my/planification'], type='http', auth="user", website=True)
# 	def my_planification_search(self, date_start='', date_end='', referent='', agence='', equipe=''):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				partner = request.env.user.partner_id
# 				# audit_suivant date_dernier_audit
# 				request_search = ""
# 				if len(date_start) > 0 and len(date_end) > 0:
# 					request_search += " AND e.audit_suivant >= '" + date_start + "' and e.audit_suivant <= '" + date_end + "'"
# 				if len(agence) > 0:
# 					request_search += " AND LOWER(agence.name) like '%" + agence.lower() + "%'"
# 				if len(equipe) > 0:
# 					request_search += " AND LOWER(equipe.name) like '%" + equipe.lower() + "%'"
# 				if len(referent) > 0:
# 					request_search += " AND LOWER(referent.name) like '%" + referent.lower() + "%'"
#
# 				request.env.cr.execute(
# 					"SELECT DISTINCT e.id FROM critt_equipment as e"
# 					" LEFT JOIN res_partner as equipe ON equipe.id = e.equipe_id"
# 					" LEFT JOIN res_partner as agence ON agence.id = e.agence_id"
# 					" LEFT JOIN res_partner as referent ON referent.id = e.referent"
# 					" WHERE e.owner_user_id = " + str(request.env.user.id) + request_search,
# 				)
#
# 				test = "SELECT DISTINCT e.id FROM critt_equipment as e" \
# 					   " LEFT JOIN res_partner as equipe ON equipe.id = e.equipe_id" \
# 					   " LEFT JOIN res_partner as agence ON agence.id = e.agence_id" \
# 					   " LEFT JOIN res_partner as referent ON referent.id = e.referent" \
# 					   " WHERE e.owner_user_id = " + str(request.env.user.id) + request_search
#
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				equipments = request.env['critt.equipment'].sudo().browse(ids)
#
# 				# equipments = equipments + equipments+ equipments+ equipments+ equipments+ equipments+ equipments+ equipments+ equipments+ equipments
#
# 				return request.render("certification.my_planification",
# 										{
# 											'user': request.env.user,
# 											'partner': partner,
# 											'equipments': equipments,
# 											'date_start': date_start,
# 											'date_end': date_end,
# 											'referent': referent,
# 											'agence': agence,
# 											'equipe': equipe,
# 											'test': test
# 										})
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route(['/my/equipments', '/my/equipments/tracking/save'], type='http', auth="user", website=True)
# 	def portal_my_tracking_save(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				#request.env.cr.execute("UPDATE res_partner SET street='3 ruee Ernest Perochon' WHERE id =7")
#
# 				partner = request.env['res.partner'].sudo().browse(int(request.env.user.partner_id.id))
# 				#equip = request.env['critt.equipment'].browse(int(equipment_id))
# 				template = {
# 					'company_name': post['company_name'],
# 					'phone': post['phone'],
# 					'email': post['email'],
# 					'website': post['website']
# 				}
# 				partner.sudo().write(template)
#
# 				if post.get('removePhoto') == '1':
# 					self._remove_partner_image(request, partner)
# 				if post.get('partner_image'):
# 					file = post.get('partner_image')
# 					self._set_partner_image(request, file, partner)
#
# 				return request.redirect('/my/equipments/tracking')
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	#list materiels
# 	@http.route(['/my/equipments', '/my/equipments'], type='http', auth="user", website=True)
# 	def portal_my_equipments(self, search='', search_qr_code='', **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
#
# 				#if request.env.user.gest_materiel == False:
# 				#	return request.redirect('/')
#
# 				partner = request.env.user.partner_id
#
# 				search_qr_code_result = -1
# 				if len(search_qr_code) > 0:
# 					search_qr_code_result = 1
# 					equipments = request.env['critt.equipment'].search(
# 						['&', ('owner_user_id', '=', request.env.user.id), '|',('qr_code', '=', search_qr_code), ('num_materiel', '=', search_qr_code)])
# 					if len(equipments) == 1:
# 						Horodating = request.env['critt.horodating']
#
# 						vals = {'user': request.env.user.id, 'action': "Recherche QR Code", 'equipment_id': equipments[0].id}
#
# 						Horodating.create(vals)
#
# 						return request.redirect('/my/equipment/%s' % (equipments[0].id))
#
#
#
# 				# audit_suivant date_dernier_audit
# 				# request_string = " AND ("
# 				# request_string += "LOWER(num_materiel) like '%" + search.lower() + "%'"
# 				# request_string += " OR LOWER(name) like '%" + search.lower() + "%'"
# 				# request_string += " OR LOWER(internal_no) like '%" + search.lower() + "%'"
# 				# request_string += " OR LOWER(agence) like '%" + search.lower() + "%'"
# 				# request_string += " OR LOWER(equipe) like '%" + search.lower() + "%'"
# 				# request_string += " )"
# 				# request.env.cr.execute(
# 				# 	"SELECT DISTINCT id FROM critt_equipment "
# 				# 	"WHERE owner_user_id = %s" + request_string,
# 				# 	(request.env.user.id,))
# 				#
# 				# ids = [x[0] for x in request.env.cr.fetchall()]
# 				# equipments = request.env['critt.equipment'].sudo().browse(ids)
# 				if len(search) == 0:
# 					equipments = request.env['critt.equipment'].search(
# 						[('owner_user_id', '=', request.env.user.id)], order='num_materiel asc')
# 				else:
# 					request_string = " AND ("
# 					request_string += "LOWER(e.num_materiel) like '%" + search.lower() + "%'"
# 					request_string += " OR LOWER(e.name) like '%" + search.lower() + "%'"
# 					request_string += " OR LOWER(e.internal_no) like '%" + search.lower() + "%'"
# 					request_string += " OR LOWER(agence.name) like '%" + search.lower() + "%'"
# 					request_string += " OR LOWER (equipe.name) like '%" + search.lower() + "%'"
# 					request_string += " OR LOWER(c.name) like '%" + search.lower() + "%'"
# 					request_string += " )"
# 					#request_string = "LOWER(num_materiel) like '%" + search.lower() + "%'"
# 					request.env.cr.execute(
# 						"SELECT DISTINCT e.id, e.num_materiel FROM critt_equipment as e JOIN critt_equipment_category as c ON c.id = e.category_id"
# 						" LEFT JOIN res_partner as equipe ON equipe.id = e.equipe_id"
# 						" LEFT JOIN res_partner as agence ON agence.id = e.agence_id"
# 						" WHERE e.owner_user_id = " + str(request.env.user.id) + request_string + " ORDER BY e.num_materiel",
# 						)
#
# 					ids = [x[0] for x in request.env.cr.fetchall()]
# 					equipments = request.env['critt.equipment'].sudo().browse(ids)
# 					#equipments = request.env['critt.equipment'].search(
# 					#['&', ('owner_user_id', '=', request.env.user.id),
# 					# ('|', ('num_materiel', 'ilike', search), ('|', ('name', 'ilike', search),
# 					#	   ('|', ('num_materiel', 'ilike', search), ('|', ('agence', 'ilike', search), ('equipe', 'ilike', search)))))])
#
#
#
# 				return request.render("certification.my_equipments",
# 									  {
# 										  'user': request.env.user,
# 										  'partner': partner,
# 										  'equipments': equipments,
# 										  'search': search,
# 										  'search_qr_code_result': search_qr_code_result,
# 										  'search_qr_code': search_qr_code,
# 									  })
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# FICHE EQUIPMENT
# 	@route(['/my', '/my/equipment/<int:equipment_id>'], type='http', auth="user", website=True)
# 	def portal_my_equipment(self, equipment_id, **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				#if request.env.user.gest_materiel == False:
# 				#	return request.redirect('/')
#
# 				Equipment = request.env['critt.equipment']
#
# 				#equipment = request.env['critt.equipment'].search([('id', '=', equipment_id)])
# 				equipment = request.env['critt.equipment'].search(
# 					[('id', '=', int(equipment_id)), ('owner_user_id', '=', request.env.user.id)])
# 				categories = request.env['critt.equipment.category'].sudo().search([])
#
# 				# saleOrders = []
# 				# saleOrderLineEquipment = request.env['critt.certification.audit'].sudo().search([('equipement', '=', equipment.id)])
# 				# files = request.env['ir.attachment'].sudo().search([('res_id', '=', equipment_id)])
# 				# files = request.env['ir.attachment'].sudo().search([('id', '=', 1120)])
# 				# files = request.env['ir.attachment'].sudo().search([
# 				#    ('res_model', '=', 'critt.equipment'),
# 				#    ('res_id', '=', 86)
# 				# ])
#
# 				rapportsVGP = []
# 				for rapport in equipment.rapport_controle:
# 					list_id_rapports_vgp = []
# 					list_id_rapports_vgp.append(rapport.id)
# 				rapportsVGP = request.env['critt.certification.rapport_controle'].sudo().browse([29,28])
#
#
# 				request.env.cr.execute(
# 					"""SELECT *
# 					  FROM public.critt_certification_certificat
# 					  WHERE id_equipment = %s AND pdf IS NOT NULL
# 					  ORDER BY sequence ASC, date DESC""",
# 					(equipment_id,))
#
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				certificats = request.env['critt.certification.certificat'].sudo().browse(ids)
#
# 				# request.env.cr.execute("SELECT DISTINCT id FROM ir_attachment WHERE res_model = 'critt.equipment' AND res_id = %s", (equipment_id,))
# 				#request.env.cr.execute(
# 				#	"SELECT DISTINCT id, certificat_date FROM ir_attachment WHERE name NOT IN ('image', 'image_medium', 'image_small') AND res_model = 'critt.equipment' AND res_id = %s ORDER BY certificat_date DESC",
# 				#	(equipment_id,))
#
# 				request.env.cr.execute(
# 					"""SELECT *
# 					  FROM public.critt_certification_certificat
# 					  WHERE id_equipment = %s AND dl_pdf IS NOT NULL
# 					  ORDER BY sequence ASC, date DESC""",
# 					(equipment_id,))
#
# 				idsOther = [x[0] for x in request.env.cr.fetchall()]
# 				otherCertificats = request.env['critt.certification.certificat'].sudo().browse(idsOther)
#
# 				# files = request.env['ir.attachment'].sudo().search([('res_name', '=', "toto/zdqsdqsd")])
#
# 				# request.env.cr.execute(
# 				# 	"""select invo.id
#                 #     FROM account_move as invo
#                 #     JOIN sale_order as ord ON ord.name = invo.invoice_origin
#                 #     JOIN critt_sale_order_line_equipment as csole ON csole.order_id = ord.id
#                 #     WHERE ord.partner_id = %s AND csole.equipment_id = %s AND invo.state = 'posted'""",
# 				# 	(request.env.user.partner_id.id, equipment.id,))
# 				request.env.cr.execute(
# 						"""SELECT DISTINCT so.id
# 							FROM critt_sale_order_line_equipment as csole
# 							JOIN sale_order so ON csole.order_id = so.id
# 							JOIN account_move invoice ON invoice.invoice_origin = so.name
# 							JOIN critt_equipment e ON csole.equipment_id = e.id
# 							WHERE csole.equipment_id = %s AND e.derniere_facture IS NOT NULL""",
# 					(equipment_id,))
#
# 				invoices_ids = [x[0] for x in request.env.cr.fetchall()]
# 				invoices = request.env['sale.order'].sudo().browse(invoices_ids)
#
# 				#for order in orders:
# 					#test = 'c'
# 					#request.env.cr.execute(
# 					#	"SELECT DISTINCT id, certificat_date FROM ir_attachment WHERE name NOT IN ('image', 'image_medium', 'image_small') AND res_model = 'critt.equipment' AND res_id = %s ORDER BY certificat_date DESC",
# 					#	(equipment_id,))
#
# 					#attachement_ids = [x[0] for x in request.env.cr.fetchall()]
# 					#invoices = request.env['ir.attachment'].sudo().browse(attachement_ids)
# 					#tmp = request.env['account.move'].sudo().search(
# 					#[('origin', '=', orders.order_id.name)])
# 					#for item in tmp:
# 					#	invoices.append(item)
# 					#invoices = tmp
#
# 				request.env.cr.execute(
# 					"""SELECT * FROM sale_order AS so
# 					 JOIN critt_sale_order_line_equipment AS csole ON so.id = csole.order_id
# 					 WHERE so.partner_id = %s AND csole.equipment_id = %s""", (request.env.user.partner_id.id, equipment_id,))
#
# 				sale_orders_ids = [x[0] for x in request.env.cr.fetchall()]
# 				sale_orders = request.env['sale.order'].sudo().browse(sale_orders_ids)
#
# 				return request.render("certification.portal_my_equipment_fiche",
# 									  {
# 										  'equipment': equipment,
# 										  'rapportsVGP': rapportsVGP,
# 										  'categories': categories,
# 										  'certificats': certificats,
# 										  'otherCertificats': otherCertificats,
# 										  'invoices': invoices,
# 										  'sale_orders': sale_orders,
# 									  })
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# equipment form create/edit
# 	@http.route(['/my/', '/my/equipment'], type='http', auth="user", website=True)
# 	def portal_equipment(self, id='', **kw):
# 		if request.env.user.has_group('certification.website_lvl_2') or request.env.user.has_group('certification.certification_lvl_3'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				# if request.env.user.gest_materiel == False:
# 				# 	return request.redirect('/')
#
# 				create = True
# 				certificats = []
# 				otherCertificats = []
# 				invoices = []
# 				sale_orders = []
# 				if id:
# 					equipment = request.env['critt.equipment'].search(
# 						[('id', '=', int(id)), ('owner_user_id', '=', request.env.user.id)])
# 					if equipment:
# 						# si l'equipment est géré par cap levage, on interdit l'affichage du formulaire d'édition
# 						create = False
# 						if request.env.user.gest_materiel == False:
# 							return request.redirect('/my/equipment/' + str(equipment.id))
#
# 						# request.env.cr.execute(
# 						#	"SELECT DISTINCT id, sequence_certificat FROM ir_attachment WHERE type_certificat IN ('creation', 'control', 'reforme') AND res_model = 'critt.equipment' AND res_id = %s ORDER BY sequence_certificat ASC",
# 						#	(equipment.id,))
#
# 						# attachement_ids = [x[0] for x in request.env.cr.fetchall()]
# 						# files = request.env['ir.attachment'].sudo().browse(attachement_ids)
#
# 						# liste des certificats de cap levage
# 						request.env.cr.execute(
# 							"""SELECT *
# 							  FROM public.critt_certification_certificat
# 							  WHERE id_equipment = %s AND pdf IS NOT NULL
# 							  ORDER BY sequence ASC, date DESC""",
# 							(equipment.id,))
#
# 						ids = [x[0] for x in request.env.cr.fetchall()]
# 						certificats = request.env['critt.certification.certificat'].sudo().browse(ids)
#
# 						# liste des certificats externe
# 						request.env.cr.execute(
# 							"""SELECT *
# 							  FROM public.critt_certification_certificat
# 							  WHERE id_equipment = %s AND dl_pdf IS NOT NULL
# 							  ORDER BY sequence ASC, date DESC""",
# 							(equipment.id,))
#
# 						idsOther = [x[0] for x in request.env.cr.fetchall()]
# 						otherCertificats = request.env['critt.certification.certificat'].sudo().browse(idsOther)
#
# 						request.env.cr.execute(
# 							"""SELECT DISTINCT so.id
#                                 FROM critt_sale_order_line_equipment as csole
#                                 JOIN sale_order so ON csole.order_id = so.id
#                                 JOIN account_move invoice ON invoice.invoice_origin = so.name
#                                 JOIN critt_equipment e ON csole.equipment_id = e.id
#                                 WHERE csole.equipment_id = %s AND e.derniere_facture IS NOT NULL""",
# 							(equipment.id,))
#
# 						invoices_ids = [x[0] for x in request.env.cr.fetchall()]
# 						invoices = request.env['sale.order'].sudo().browse(invoices_ids)
#
# 						request.env.cr.execute(
# 							"""SELECT * FROM sale_order AS so
#                              JOIN critt_sale_order_line_equipment AS csole ON so.id = csole.order_id
#                              WHERE so.partner_id = %s AND csole.equipment_id = %s""",
# 							(request.env.user.partner_id.id, equipment.id,))
#
# 						sale_orders_ids = [x[0] for x in request.env.cr.fetchall()]
# 						sale_orders = request.env['sale.order'].sudo().browse(sale_orders_ids)
#
# 				if create:
# 					# interdication d'accéder au formulaire de création si le niveau n'est pas au minimum de 3
# 					if not request.env.user.has_group('certification.website_lvl_3'):
# 						return request.render("website.homepage")
# 					equipment = request.env['critt.equipment'].new({
# 						'name': '',
# 						'orga_certif': '',
# 						'of_cap_levage': False
# 					})
#
# 				equipment_create_right_ids = request.env['critt.equipment.create_right'].sudo().search([('res_partner_id', '=', request.env.user.partner_id.id)])
#
# 				equipment_create_right_list_ids = []
# 				for equipment_create_right_id in equipment_create_right_ids:
# 					equipment_create_right_list_ids.append(equipment_create_right_id.id)
#
# 				categories = request.env['critt.equipment.category'].sudo().search([('equipment_create_right_ids', 'in', equipment_create_right_list_ids)])
#
# 				organismes = request.env['critt.equipment.organisme'].sudo().search([])
#
# 				fabricants = request.env['critt.equipment.fabricant'].sudo().search([])
#
# 				#equipes = request.env['critt.equipment.equipe'].sudo().search(
# 				#	[('owner_user_id', '=', request.env.user.id)])
# 				#agences = request.env['critt.equipment.agence'].sudo().search(
# 				#	[('owner_user_id', '=', request.env.user.id)])
#
# 				equipes = request.env['res.partner'].sudo().search(
# 					[('parent_id', '=', request.env.user.partner_id.id), ('type', '=', 'contact'), ])
#
# 				agences = request.env['res.partner'].sudo().search(
# 					[('parent_id', '=', request.env.user.partner_id.id), ('type', '=', 'delivery'), ])
#
# 				referents = request.env['res.partner'].sudo().search([('parent_id', '=', request.env.user.partner_id.id)])
#
# 				values = {
# 					'equipment_create_right_ids': equipment_create_right_ids,
# 					'equipment': equipment,
# 					'categories': categories,
# 					'fabricants': fabricants,
# 					'organismes': organismes,
# 					'equipes': equipes,
# 					'agences': agences,
# 					'create': create,
# 					'certificats': certificats,
# 					'referents': referents,
# 					'otherCertificats': otherCertificats,
# 					'invoices': invoices,
# 					'sale_orders': sale_orders
# 				}
#
# 				if equipment.of_cap_levage:
# 					# return request.redirect('/my/equipment/' + str(equipment.id))
# 					return request.render("certification.portal_my_equipment_light_edit", values)
#
# 				return request.render("certification.portal_my_equipment", values)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# SAVE/create EQUIPMENT
# 	@http.route(['/my/equipment/save'], type='http', auth='user', website=True)
# 	def save(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				equipment_id = post['id']
#
# 				if int(equipment_id) == 0:
# 					create = True
# 				else:
# 					equip = request.env['critt.equipment'].browse(int(equipment_id))
# 					create = False
# 				#odoo.exceptions.ValidationError: ('Ce num곯 de mat곩el existe dꫠ', None)
#
# 				#if isinstance(equipment_id, numbers.Integral):
# 				#	equip = request.env['critt.equipment'].browse(int(equipment_id))
# 				#	if equip:
# 				#		create = False
# 				#	else:
# 				#		create = True
# 				#else:
# 				#	create = True
#
# 				#if post.get('of_cap_levage'):
# 				#	of_cap_levage = True
# 				#else:
# 				#	of_cap_levage = False
#
#
# 				try:
# 					date_dernier_audit = datetime.datetime.strptime(post['date_dernier_audit'], '%d/%m/%Y').date()
# 				except:
# 					date_dernier_audit = None
#
# 				try:
# 					audit_suivant = datetime.datetime.strptime(post['date_audit_suivant'], '%d/%m/%Y').date()
# 				except:
# 					audit_suivant = None
#
# 				try:
# 					an_mise_service = datetime.datetime.strptime(post['an_mise_service'], '%d/%m/%Y').date()
# 				except:
# 					an_mise_service = None
#
# 				fabricant_id = None
# 				if int(post['fabricant_id']) != -1:
# 					fabricant_id = post['fabricant_id']
#
# 				organisme_id = None
# 				if int(post['organisme_id']) != -1:
# 					organisme_id = int(post['organisme_id'])
#
# 				category_id = None
# 				if int(post['category_id']) != -1:
# 					category_id = int(post['category_id'])
#
# 				display_cmu = False
# 				display_tmu = False
# 				display_model = False
# 				display_longueur = False
# 				display_nombre_brins = False
# 				display_diametre = False
# 				display_grade = False
# 				display_num_lot = False
# 				display_num_commande = False
# 				if int(post['category_id']) != -1:
# 					category = request.env['critt.equipment.category'].search([('id', '=', category_id)])
# 					of_cap_levage = category.of_cap_levage
# 					display_cmu = category.display_cmu
# 					display_tmu = category.display_tmu
# 					display_model = category.display_model
# 					display_longueur = category.display_longueur
# 					display_nombre_brins = category.display_nombre_brins
# 					display_diametre = category.display_diametre
# 					display_grade = category.display_grade
# 					display_num_lot = category.display_num_lot
# 					display_num_commande = category.display_num_commande
#
#
# 				equipe_id = None
# 				if len(post['equipeAdd']) > 0:
# 					# create equipe
# 					newEquipe = request.env['res.partner'].sudo().create({'name': post['equipeAdd'], 'parent_id': request.env.user.partner_id.id, 'type': 'contact', 'active': True, 'display_name': post['equipeAdd'],})
# 					equipe_id = newEquipe.id
# 				else:
# 					if int(post['equipe']) != -1:
# 						equipe_id = int(post['equipe'])
#
# 				agence_id = None
# 				if len(post['agenceAdd']) > 0:
# 					# create agence
# 					newAgence = request.env['res.partner'].sudo().create({'name': post['agenceAdd'], 'parent_id': request.env.user.partner_id.id, 'type': 'delivery', 'active': True, 'display_name': post['equipeAdd'],})
# 					agence_id = newAgence.id
# 				else:
# 					if int(post['agence']) != -1:
# 						agence_id = int(post['agence'])
#
# 				internal_no = post['internal_no']
# 				if len(internal_no) == 0:
# 					internal_no = None
#
# 				referent = None
# 				if int(post['referent']) != -1:
# 					referent = int(post['referent'])
#
# 				# referent = int(post['referent'])
# 				# if len(referent) == 0 or referent == "-1":
# 				# 	referent = None
#
# 				observ_blocage = post.get('observ_blocage')
# 				if len(observ_blocage) == 0:
# 					observ_blocage = None
#
# 				date_fabrication = post.get('date_fabrication')
# 				if len(date_fabrication) == 0:
# 					date_fabrication = None
#
# 				# nfc = post['nfc']
# 				# if len(nfc) == 0:
# 				# 	nfc = None
#
# 				model = post.get('model')
# 				if len(model) == 0:
# 					model = None
#
# 				last_general_observation = post.get('last_general_observation')
# 				if len(last_general_observation) == 0:
# 					last_general_observation = None
#
# 				qr_code = post.get('qr_code')
# 				if len(qr_code) == 0:
# 					qr_code = None
#
# 				if post.get('is_bloque') == '1':
# 					Horodating = request.env['critt.horodating']
# 					vals = {'user': request.env.user.id, 'action': "Blocage matériel", 'equipment_id': equipment_id}
# 					Horodating.create(vals)
# 					is_bloque = True
# 					date_bloque = date.today()
# 				else:
# 					is_bloque = False
# 					date_bloque = None
#
# 				cmu = ''
# 				if post.get('cmu'):
# 					cmu = post['cmu']
# 				nombre_brins = 0
# 				if post.get('nombre_brins'):
# 					nombre_brins = post['nombre_brins']
# 				longueur = 0
# 				if post.get('longueur'):
# 					longueur = post['longueur']
# 				tmu = ''
# 				if post.get('tmu'):
# 					tmu = post['tmu']
# 				model = ''
# 				if post.get('model'):
# 					model = post['model']
# 				diametre = 0
# 				if post.get('diametre'):
# 					diametre = post['diametre']
# 				grade = ''
# 				if post.get('grade'):
# 					grade = post['grade']
# 				num_lot = ''
# 				if post.get('num_lot'):
# 					num_lot = post['num_lot']
# 				num_commande = ''
# 				if post.get('num_commande'):
# 					num_commande = post['num_commande']
#
#
# 				template = {
# 					#'name': post['name'],
# 					'owner_user_id': request.env.user.id,
# 					'res_partner_id': request.env.user.partner_id.id,
# 					'num_materiel': post['num_materiel'],
# 					'internal_no': internal_no,
# 					'referent': referent,
# 					'category_id': category_id,
# 					'an_mise_service': an_mise_service,
# 					'date_dernier_audit': date_dernier_audit,
# 					'audit_suivant': audit_suivant,
# 					# 'nfc': nfc,
# 					'equipe_id': equipe_id,
# 					'agence_id': agence_id,
# 					'fabricant_id': fabricant_id,
# 					'model': model,
# 					'cmu': cmu,
# 					'tmu': tmu,
#                     'num_commande': num_commande,
#                     'num_lot': num_lot,
# 					'diametre': diametre,
# 					'grade': grade,
# 					'nombre_brins': nombre_brins,
# 					'longueur': longueur,
# 					'of_cap_levage': of_cap_levage,
# 					'display_cmu': display_cmu,
# 					'display_tmu': display_tmu,
# 					'display_model': display_model,
# 					'display_longueur': display_longueur,
# 					'display_nombre_brins': display_nombre_brins,
# 					'display_diametre': display_diametre,
# 					'display_grade': display_grade,
# 					'display_num_lot': display_num_lot,
# 					'display_num_commande': display_num_commande,
# 					'from_cap_levage': False,
# 					'organisme_id': organisme_id,
# 					#'orga_certif': post['orga_certif'],
# 					'is_bloque': is_bloque,
# 					'date_bloque': date_bloque,
# 					#'localisation_description': post['localisation_description'],
# 					'periode': post['periode'],
# 					'qr_code': qr_code,
# 					'last_general_observation': last_general_observation,
# 					'observ_blocage': observ_blocage,
# 					'date_fabrication': date_fabrication,
#
# 					# '': 'https://parismatch.be/app/uploads/2018/04/Macaca_nigra_self-portrait_large-e1524567086123-1100x715.jpg'
# 				}
#
# 				if create:
# 					equip = request.env['critt.equipment']
# 					newEquip = equip.sudo().create(template)
#
# 					# res = False
# 					# try:
# 					# 	newEquip = equip.sudo().create(template)
# 					# 	res = True
# 					# except Exception as e:
# 					# 	error = str(e)
# 					# 	res = False
# 					# 	#return request.redirect('http://www.google.fr')
#
#
# 					# add image
# 					if post.get('equipment_image'):
# 						file = post.get('equipment_image')
# 						try:
# 							self._set_equipment_image(request, file, newEquip)
# 						except:
# 							error = 'error create photo'
#
#
# 					# add certificats externes
# 					if request.env.user.gest_materiel:
# 						index = 1
# 						while post.get('certificat_attachment_' + str(index), False):
# 							file = post.get('certificat_attachment_' + str(index))
# 							#date = post['certificat_date_' + str(index)]
# 							#orga_certif = post['certificat_orga_certif_' + str(index)]
# 							description = post['certificat_description_' + str(index)]
# 							type = post['certificat_type_' + str(index)]
# 							self._createAttachment(file, type, description, newEquip.id)
# 							index += 1
#
# 					return request.redirect('/my/equipment/' + str(newEquip.id))
# 				else:
# 					equip.write(template)
#
# 					if post.get('removePhoto') == '1':
# 						self._remove_equipment_image(request, equip)
# 					if post.get('equipment_image'):
# 						file = post.get('equipment_image')
# 						self._set_equipment_image(request, file, equip)
#
# 					# remove attachment
# 					if request.env.user.gest_materiel:
# 						if post['filesToDelete']:
# 							idsAttachmentToDelete = post['filesToDelete'].split(',')
# 							for tmp in idsAttachmentToDelete:
# 								if (tmp.isdigit()):
# 									idCertificat = int(tmp)
# 									certificatToDelete = request.env['critt.certification.certificat'].browse(int(idCertificat))
# 									certificatToDelete.sudo().unlink()
#
# 					# write attachment
# 					if request.env.user.gest_materiel:
# 						#request.env.cr.execute(
# 						#	"SELECT DISTINCT id, sequence_certificat FROM ir_attachment WHERE type_certificat IN ('creation', 'control', 'reforme') AND res_model = 'critt.equipment' AND res_id = %s ORDER BY sequence_certificat ASC",
# 						#	(equipment_id,))
# 						request.env.cr.execute(
# 							"""SELECT *
# 							  FROM public.critt_certification_certificat
# 							  WHERE id_equipment = %s AND dl_pdf IS NOT NULL
# 							  ORDER BY sequence ASC, date DESC""",
# 							(equipment_id,))
#
# 						otherCertificat_ids = [x[0] for x in request.env.cr.fetchall()]
# 						for certificat_id in otherCertificat_ids:
# 							if post['certificat_description_edit_' + str(certificat_id)]:
# 								#try:
# 								#    certificat_date = datetime.datetime.strptime(post['certificat_date_edit_' + str(attachement_id)],
# 								#                                                 '%d/%m/%Y').date()
# 								#except:
# 								#    certificat_date = None
#
# 								attachment = request.env['critt.certification.certificat'].browse(certificat_id)
# 								template = {
# 									'desc': post['certificat_description_edit_' + str(certificat_id)]
# 									#'orga_certif': post['certificat_orga_certif_edit_' + str(attachement_id)],
# 									#'certificat_date': certificat_date
# 								}
# 								attachment.sudo().write(template)
#
# 					# add attachment
# 					if request.env.user.gest_materiel:
# 						index = 1
# 						while post.get('certificat_attachment_' + str(index), False):
# 							file = post.get('certificat_attachment_' + str(index))
# 							#date = post['certificat_date_' + str(index)]
# 							#orga_certif = post['certificat_orga_certif_' + str(index)]
# 							description = post['certificat_description_' + str(index)]
# 							type = post['certificat_type_' + str(index)]
# 							self._createAttachment(file, type, description, equipment_id)
# 							index += 1
#
# 				return request.redirect('/my/equipment/' + equipment_id)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route(['/my/equipment/save_light_edit'], type='http', auth='user', website=True)
# 	def save_light_edit(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				equipment_id = post['id']
#
# 				equip = request.env['critt.equipment'].browse(int(equipment_id))
# 				# odoo.exceptions.ValidationError: ('Ce num곯 de mat곩el existe dꫠ', None)
#
# 				# if isinstance(equipment_id, numbers.Integral):
# 				#	equip = request.env['critt.equipment'].browse(int(equipment_id))
# 				#	if equip:
# 				#		create = False
# 				#	else:
# 				#		create = True
# 				# else:
# 				#	create = True
#
# 				# if post.get('of_cap_levage'):
# 				#	of_cap_levage = True
# 				# else:
# 				#	of_cap_levage = False
#
# 				internal_no = post.get('internal_no')
# 				if len(internal_no) == 0:
# 					internal_no = None
#
# 				referent = None
# 				if int(post['referent']) != -1:
# 					referent = int(post['referent'])
#
# 				# referent = int(post['referent'])
# 				# if len(referent) == 0 or referent == "-1":
# 				# 	referent = None
#
# 				# nfc = post['nfc']
# 				# if len(nfc) == 0:
# 				# 	nfc = None
#
# 				if post.get('is_bloque') == '1':
# 					Horodating = request.env['critt.horodating']
# 					vals = {'user': request.env.user.id, 'action': "Blocage matériel", 'equipment_id': equipment_id}
# 					Horodating.create(vals)
# 					is_bloque = True
# 					date_bloque = date.today()
# 				else:
# 					is_bloque = False
# 					date_bloque = None
#
# 				equipe_id = None
# 				if len(post['equipeAdd']) > 0:
# 					# create equipe
# 					newEquipe = request.env['res.partner'].sudo().create(
# 						{'name': post['equipeAdd'], 'parent_id': request.env.user.partner_id.id, 'type': 'contact', 'active': True, 'display_name': post['equipeAdd'], })
# 					equipe_id = newEquipe.id
# 				else:
# 					if int(post['equipe']) != -1:
# 						equipe_id = int(post['equipe'])
#
# 				model = post.get('model')
# 				if model:
# 					if len(model) == 0:
# 						model = None
#
# 				agence_id = None
# 				if len(post['agenceAdd']) > 0:
# 					# create agence
# 					newAgence = request.env['res.partner'].sudo().create(
# 						{'name': post['agenceAdd'], 'parent_id': request.env.user.partner_id.id, 'type': 'delivery', 'active': True, 'display_name': post['agenceAdd'], })
# 					agence_id = newAgence.id
# 				else:
# 					if int(post['agence']) != -1:
# 						agence_id = int(post['agence'])
#
# 				qr_code = post.get('qr_code')
# 				if len(qr_code) == 0:
# 					qr_code = None
#
# 				last_general_observation = post.get('last_general_observation')
# 				if len(last_general_observation) == 0:
# 					last_general_observation = None
#
# 				template = {
# 					# 'name': post['name'],
# 					'internal_no': internal_no,
# 					'referent': referent,
# 					# 'nfc': nfc,
# 					'model': model,
# 					'equipe_id': equipe_id,
# 					'agence_id': agence_id,
# 					'is_bloque': is_bloque,
# 					'date_bloque': date_bloque,
# 					'qr_code': qr_code,
# 					'last_general_observation': last_general_observation,
# 					# 'localisation_description': post['localisation_description'],
#
# 					# '': 'https://parismatch.be/app/uploads/2018/04/Macaca_nigra_self-portrait_large-e1524567086123-1100x715.jpg'
# 				}
#
# 				equip.write(template)
#
# 				# remove attachment
# 				if request.env.user.gest_materiel:
# 					if post['filesToDelete']:
# 						idsAttachmentToDelete = post['filesToDelete'].split(',')
# 						for tmp in idsAttachmentToDelete:
# 							if (tmp.isdigit()):
# 								idCertificat = int(tmp)
# 								certificatToDelete = request.env['critt.certification.certificat'].browse(int(idCertificat))
# 								certificatToDelete.sudo().unlink()
#
# 				# write attachment
# 				if request.env.user.gest_materiel:
# 					# request.env.cr.execute(
# 					#	"SELECT DISTINCT id, sequence_certificat FROM ir_attachment WHERE type_certificat IN ('creation', 'control', 'reforme') AND res_model = 'critt.equipment' AND res_id = %s ORDER BY sequence_certificat ASC",
# 					#	(equipment_id,))
# 					request.env.cr.execute(
# 						"""SELECT *
# 						  FROM public.critt_certification_certificat
# 						  WHERE id_equipment = %s AND dl_pdf IS NOT NULL
# 						  ORDER BY sequence ASC, date DESC""",
# 						(equipment_id,))
#
# 					otherCertificat_ids = [x[0] for x in request.env.cr.fetchall()]
# 					for certificat_id in otherCertificat_ids:
# 						if post['certificat_description_edit_' + str(certificat_id)]:
# 							# try:
# 							#    certificat_date = datetime.datetime.strptime(post['certificat_date_edit_' + str(attachement_id)],
# 							#                                                 '%d/%m/%Y').date()
# 							# except:
# 							#    certificat_date = None
#
# 							attachment = request.env['critt.certification.certificat'].browse(certificat_id)
# 							template = {
# 								'desc': post['certificat_description_edit_' + str(certificat_id)]
# 								# 'orga_certif': post['certificat_orga_certif_edit_' + str(attachement_id)],
# 								# 'certificat_date': certificat_date
# 							}
# 							attachment.sudo().write(template)
#
# 				# add attachment
# 				if request.env.user.gest_materiel:
# 					index = 1
# 					while post.get('certificat_attachment_' + str(index), False):
# 						file = post.get('certificat_attachment_' + str(index))
# 						# date = post['certificat_date_' + str(index)]
# 						# orga_certif = post['certificat_orga_certif_' + str(index)]
# 						description = post['certificat_description_' + str(index)]
# 						type = post['certificat_type_' + str(index)]
# 						self._createAttachment(file, type, description, equipment_id)
# 						index += 1
#
# 				return request.redirect('/my/equipment/' + equipment_id)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# SAVE/create référents
# 	@http.route(['/my/referents/save'], type='http', auth='user', website=True)
# 	def saveReferents(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group(
# 				'certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				partner = request.env.user.partner_id
#
# 				# suppression du lien entre des référents et le partner
# 				if post['referentsToDelete']:
# 					idsReferentsToDelete = post['referentsToDelete'].split(',')
# 					for tmp in idsReferentsToDelete:
# 						if (tmp.isdigit()):
# 							idReferent = int(tmp)
# 							referentToUnlink = request.env['res.partner'].sudo().browse(int(idReferent))
# 							template = {
# 								'parent_id': None
# 							}
# 							referentToUnlink.sudo().write(template)
#
# 				# update all referents
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM res_partner "
# 					"WHERE parent_id = %s",
# 					(partner.id,))
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				referents = request.env['res.partner'].sudo().browse(ids)
# 				for referentEdit in referents:
# 					if post['referent_name_edit_' + str(referentEdit.id)]:
# 						agence = post['referent_agence_edit_' + str(referentEdit.id)]
# 						agence_id = None
# 						if len(agence) > 0:
# 							# creation new agence
# 							# newAgence = request.env['critt.equipment.agence'].sudo().create(
# 							#	{'name': agence, 'owner_user_id': request.env.user.id, })
# 							newAgence = request.env['res.partner'].sudo().create(
# 								{'name': agence, 'parent_id': partner.id, 'type': 'delivery', 'active': True,
# 								 'display_name': equipe, })
# 							agence_id = newAgence.id
# 						else:
# 							agence_id = int(post['referent_agence_id_edit_' + str(referentEdit.id)])
# 							if agence_id == -1:
# 								agence_id = None
#
# 						equipe = post['referent_equipe_edit_' + str(referentEdit.id)]
# 						equipe_id = None
# 						if len(equipe) > 0:
# 							# creation new equipe
# 							# newEquipe = request.env['critt.equipment.equipe'].sudo().create(
# 							#	{'name': equipe, 'owner_user_id': request.env.user.id, })
# 							newEquipe = request.env['res.partner'].sudo().create(
# 								{'name': equipe, 'parent_id': partner.id, 'type': 'contact', 'active': True,
# 								 'display_name': equipe, })
# 							equipe_id = newEquipe.id
# 						else:
# 							equipe_id = int(post['referent_equipe_id_edit_' + str(referentEdit.id)])
# 							if equipe_id == -1:
# 								equipe_id = None
#
# 						template = {
# 							'parent_id': request.env.user.partner_id.id,
# 							'name': post['referent_name_edit_' + str(referentEdit.id)],
# 							# 'first_name': post['referent_first_name_edit_' + str(referentEdit.id)],
# 							# 'last_name': post['referent_last_name_edit_' + str(referentEdit.id)],
# 							'display_name': post['referent_name_edit_' + str(referentEdit.id)],
# 							'email': post['referent_email_edit_' + str(referentEdit.id)],
# 							'phone': post['referent_phone_edit_' + str(referentEdit.id)],
# 							'function': post['referent_function_edit_' + str(referentEdit.id)],
# 							'equipe_id': equipe_id,
# 							'agence_id': agence_id,
# 						}
# 						referentEdit.sudo().write(template)
#
# 				# add referent(s)
# 				index = 1
# 				while post.get('referent_name_' + str(index), False):
# 					newReferent = request.env['res.partner']
#
# 					agence = post['referent_agence_' + str(index)]
# 					agence_id = None
# 					if len(agence) > 0:
# 						# creation new agence
# 						# newAgence = request.env['critt.equipment.agence'].sudo().create(
# 						#	{'name': agence, 'owner_user_id': request.env.user.id, })
# 						newAgence = request.env['res.partner'].sudo().create(
# 							{'name': agence, 'parent_id': partner.id, 'type': 'delivery', 'active': True,
# 							 'display_name': equipe, })
# 						agence_id = newAgence.id
# 					else:
# 						agence_id = int(post['referent_agence_id_' + str(index)])
# 						if agence_id == -1:
# 							agence_id = None
#
# 					equipe = post['referent_equipe_' + str(index)]
# 					equipe_id = None
# 					if len(equipe) > 0:
# 						# creation new equipe
# 						# newEquipe = request.env['critt.equipment.equipe'].sudo().create(
# 						#	{'name': equipe, 'owner_user_id': request.env.user.id, })
# 						newEquipe = request.env['res.partner'].sudo().create(
# 							{'name': equipe, 'parent_id': partner.id, 'type': 'contact', 'active': True,
# 							 'display_name': equipe, })
# 						equipe_id = newEquipe.id
# 					else:
# 						equipe_id = int(post['referent_equipe_id_' + str(index)])
# 						if equipe_id == -1:
# 							equipe_id = None
#
# 					template = {
# 						'parent_id': request.env.user.partner_id.id,
# 						'name': post['referent_name_' + str(index)],
# 						# 'first_name': post['referent_first_name_' + str(index)],
# 						# 'last_name': post['referent_last_name_' + str(index)],
# 						'display_name': post['referent_name_' + str(index)],
# 						'email': post['referent_email_' + str(index)],
# 						'phone': post['referent_phone_' + str(index)],
# 						'function': post['referent_function_' + str(index)],
# 						'equipe_id': equipe_id,
# 						'agence_id': agence_id,
# 					}
# 					newReferent = newReferent.sudo().create(template)
# 					index += 1
#
# 				return request.redirect('/my/equipments/tracking')
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# SAVE/create agences
# 	@http.route(['/my/agences/save'], type='http', auth='user', website=True)
# 	def saveAgences(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group(
# 				'certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				partner = request.env.user.partner_id
#
# 				# suppression du lien entre les agences et le partner
# 				if post['agencesToDelete']:
# 					idsAgencesToDelete = post['agencesToDelete'].split(',')
# 					for tmp in idsAgencesToDelete:
# 						if (tmp.isdigit()):
# 							idAgence = int(tmp)
# 							agenceToUnlink = request.env['res.partner'].sudo().browse(int(idAgence))
# 							template = {
# 								'parent_id': None
# 							}
# 							agenceToUnlink.sudo().write(template)
#
# 				# update all agences
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM res_partner "
# 					"WHERE parent_id = %s AND type = 'delivery'",
# 					(partner.id,))
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				agences = request.env['res.partner'].sudo().browse(ids)
# 				for agenceEdit in agences:
# 					if post.get('agence_name_edit_' + str(agenceEdit.id), False): # if post['agence_name_edit_' + str(agenceEdit.id)]:
# 						template = {
# 							'parent_id': request.env.user.partner_id.id,
# 							'name': post['agence_name_edit_' + str(agenceEdit.id)],
# 							'display_name': post['agence_name_edit_' + str(agenceEdit.id)],
# 							'email': post['agence_email_edit_' + str(agenceEdit.id)],
# 							'phone': post['agence_phone_edit_' + str(agenceEdit.id)],
# 							'mobile': post['agence_mobile_edit_' + str(agenceEdit.id)],
# 							'street': post['agence_street_edit_' + str(agenceEdit.id)],
# 							'zip': post['agence_zip_edit_' + str(agenceEdit.id)],
# 							'city': post['agence_city_edit_' + str(agenceEdit.id)]
# 						}
# 						agenceEdit.sudo().write(template)
#
# 				# add agence(s)
# 				index = 1
# 				while post.get('agence_name_' + str(index), False):
# 					newAgence = request.env['res.partner']
# 					template = {
# 						'parent_id': request.env.user.partner_id.id,
# 						'name': post['agence_name_' + str(index)],
# 						'type': 'delivery',
# 						'display_name': post['agence_name_' + str(index)],
# 						'email': post['agence_email_' + str(index)],
# 						'phone': post['agence_phone_' + str(index)],
# 						'mobile': post['agence_mobile_' + str(index)],
# 						'street': post['agence_street_' + str(index)],
# 						'zip': post['agence_zip_' + str(index)],
# 						'city': post['agence_city_' + str(index)]
# 					}
# 					newAgence = newAgence.sudo().create(template)
# 					index += 1
#
# 				return request.redirect('/my/equipments/tracking')
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# SAVE/create equipes
# 	@http.route(['/my/equipes/save'], type='http', auth='user', website=True)
# 	def saveEquipes(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group(
# 				'certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				partner = request.env.user.partner_id
#
# 				# suppression du lien entre les équipes et le partner
# 				if post['equipesToDelete']:
# 					idsEquipesToDelete = post['equipesToDelete'].split(',')
# 					for tmp in idsEquipesToDelete:
# 						if (tmp.isdigit()):
# 							idEquipe = int(tmp)
# 							equipeToUnlink = request.env['res.partner'].sudo().browse(int(idEquipe))
# 							template = {
# 								'parent_id': None
# 							}
# 							equipeToUnlink.sudo().write(template)
#
# 				# update all equipes
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM res_partner "
# 					"WHERE parent_id = %s AND type = 'contact'",
# 					(partner.id,))
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				equipes = request.env['res.partner'].sudo().browse(ids)
# 				for equipeEdit in equipes:
# 					if post.get('equipe_name_edit_' + str(equipeEdit.id), False): # post['equipe_name_edit_' + str(equipeEdit.id)]:
# 						template = {
# 							'parent_id': request.env.user.partner_id.id,
# 							'name': post['equipe_name_edit_' + str(equipeEdit.id)],
# 							'display_name': post['equipe_name_edit_' + str(equipeEdit.id)],
# 							'email': post['equipe_email_edit_' + str(equipeEdit.id)],
# 							'phone': post['equipe_phone_edit_' + str(equipeEdit.id)],
# 							'mobile': post['equipe_mobile_edit_' + str(equipeEdit.id)],
# 							'function': post['equipe_function_edit_' + str(equipeEdit.id)]
# 						}
# 						equipeEdit.sudo().write(template)
#
# 				# add equipe(s)
# 				index = 1
# 				while post.get('equipe_name_' + str(index), False):
# 					newEquipe = request.env['res.partner']
# 					template = {
# 						'parent_id': request.env.user.partner_id.id,
# 						'type': 'contact',
# 						'name': post['equipe_name_' + str(index)],
# 						'display_name': post['equipe_name_' + str(index)],
# 						'email': post['equipe_email_' + str(index)],
# 						'phone': post['equipe_phone_' + str(index)],
# 						'mobile': post['equipe_mobile_' + str(index)],
# 						'function': post['equipe_function_' + str(index)]
# 					}
# 					newEquipe = newEquipe.sudo().create(template)
# 					index += 1
#
# 				return request.redirect('/my/equipments/tracking')
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	#Devis
# 	# Devis en attente
# 	@http.route(['/my/', '/my/quotes'], type='http', auth="user", website=True)
# 	def portal_my_quotes(self, search='', **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				#if request.env.user.gest_materiel == False:
# 				#	return request.redirect('/')
#
# 				quotes = request.env['sale.order'].search(
# 					[('partner_id', '=', request.env.user.partner_id.id), ('state', 'in', ['sent'])])
# 					#[('partner_id', '=', request.env.user.partner_id.id), ('state', 'in', ['draft', 'sent'])])
#
# 				values = {
# 					'quotes': quotes
# 				}
# 				return request.render("certification.portal_my_quotes", values)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# accepter devis
# 	@http.route(['/my/quote/accept'], type='http', auth='user', website=True)
# 	def portal_my_quote_accept(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				# orders = request.httprequest.form.getlist('ordersSelected')
# 				order_id = post['order_to_update']
# 				if order_id:
# 					saleOrder = request.env['sale.order'].sudo().browse(int(order_id))
# 					if saleOrder:
# 						num_commande_client = post['num_commande_client_' + str(saleOrder.id)]
# 						template = {
# 							#'confirmation_date': now.strftime("%Y-%m-%d %H:%M:%S"),
# 							'num_commande_client': num_commande_client
# 						}
# 						done = saleOrder.sudo().write(template)
#
# 						if post.get('order_attachment_bon_commande_' + str(saleOrder.id)):
# 							file = post.get('order_attachment_bon_commande_' + str(saleOrder.id))
# 							# file = post['order_attachment_bon_commande_' + str(saleOrder.id)]
# 							self._createAttachmentBonDeCommande(file, saleOrder)
#
#
# 				# if len(orders) == 0:
# 				# 	quotes = request.env['sale.order'].search(
# 				# 		[('partner_id', '=', request.env.user.partner_id.id), ('state', 'in', ['sent'])])
# 				# 	for order in quotes:
# 				# 		val = post['num_commande_client_update_' + str(order.id)]
# 				# 		if int(val) != 0:
# 				# 			num_commande_client = post['num_commande_client_' + str(order.id)]
# 				# 			template = {
# 				# 				'num_commande_client': num_commande_client
# 				# 			}
# 				# 			done = order.sudo().write(template)
# 				#
# 				# else:
# 				# 	done = False
# 				# 	now = datetime.datetime.now()
# 				# 	for order_id in orders:
# 				# 		saleOrder = request.env['sale.order'].sudo().browse(int(order_id))
# 				# 		if saleOrder:
# 				# 			num_commande_client = post['num_commande_client_' + str(saleOrder.id)]
# 				# 			template = {
# 				# 				'state': 'sale',
# 				# 				#'confirmation_date': now.strftime("%Y-%m-%d %H:%M:%S"),
# 				# 				'invoice_status': 'to invoice', # 'invoiced',
# 				# 				'num_commande_client': num_commande_client,
# 				# 				'is_validate_by_customer': True
# 				# 			}
# 				# 			done = saleOrder.sudo().write(template)
#
# 				return request.redirect('/my/quotes')
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	@http.route(['/my/quote/uploadBonCommande'], type='http', auth='user', website=True)
# 	def portal_my_quote_uploadBonCommande(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group(
# 				'certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				# orders = request.httprequest.form.getlist('ordersSelected')
# 				order_id = post['order_to_update']
# 				if order_id:
# 					saleOrder = request.env['sale.order'].sudo().browse(int(order_id))
# 					if saleOrder:
# 						if post.get('order_attachment_bon_commande_' + str(saleOrder.id)):
# 							file = post.get('order_attachment_bon_commande_' + str(saleOrder.id))
# 							# file = post['order_attachment_bon_commande_' + str(saleOrder.id)]
# 							self._createAttachmentBonDeCommande(file, saleOrder)
#
# 				return request.redirect('/my/quote/see/' + str(order_id))
# 				#return request.redirect('/my/quotes')
# 		else:
# 			return request.render("website.homepage")
#
# 	#voir devis
# 	@http.route(['/my/quote/see/<int:id>'], type='http', auth="user", website=True)
# 	def portal_see_quote(self, id="", **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				#if request.env.user.gest_materiel == False:
# 				#	return request.redirect('/')
#
# 				quote = request.env['sale.order'].search([('id', '=', id)])
# 				if quote.partner_id.id == request.env.user.partner_id.id:
# 					if quote.state not in ['sale', 'done']:
# 						auth_param = url_encode(request.env.user.partner_id.signup_get_auth_param()[quote.partner_id.id])
# 						return request.redirect(quote.get_portal_url(query_string='&%s' % auth_param))
# 					else:
# 						return request.redirect('/my/orders/%s' % quote.id)
# 				else:
# 					return request.render("website.403")
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	#AUDIT REQUEST
# 	# LIST AUDIT REQUEST
# 	@http.route(['/my/requests', '/my/requests/page/<int:page>'], type='http', auth="user", website=True)
# 	def portal_my_requests(self, page=1, date_begin=None, date_end=None, sortby=None, search=None, search_in='name', **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				values = self._prepare_portal_layout_values_requests()
# 				partner = request.env.user.partner_id
# 				SaleOrder = request.env['sale.order']
#
# 				domain = [('state', 'in', ['draft', 'sent']), ('partner_id', '=', request.env.user.partner_id.id)]
#
# 				searchbar_sortings = {
# 					'name': {'label': _('Nom'), 'order': 'name'},
# 					'state': {'label': _('État'), 'order': 'state'},
# 					'amount_total': {'label': _('Prix'), 'order': 'amount_total'}
# 				}
# 				searchbar_inputs = {
# 					'all': {'input': 'all', 'label': _('Tout')},
# 					'name': {'input': 'name', 'label': _('Nom')},
# 					'state': {'input': 'state', 'label': _('État')},
# 					'amount_total': {'input': 'amount_total', 'label': _('Prix')}
#
# 				}
#
# 				# default sortby order
# 				if not sortby:
# 					sortby = 'name'
# 				sort_order = searchbar_sortings[sortby]['order']
#
# 				# search
# 				if search and search_in:
# 					search_domain = []
# 					if search_in in ('all'):
# 						tmp = 'en cours de traitement'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'draft'
# 						tmp = 'devis envoyé'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'sent'
# 						tmp = 'bon de commande'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'sale'
# 						tmp = 'terminée'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'done'
# 						tmp = 'annulée'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'cancel'
# 					search_domain = OR(
# 							[search_domain, ['|', '|', ('name', 'ilike', search), ('state', 'ilike', search),
# 											 ('amount_total', 'ilike', search)]])
# 					if search_in in ('name'):
# 						search_domain = OR([search_domain, [('name', 'ilike', search)]])
# 					if search_in in ('state'):
# 						tmp = 'en cours de traitement'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'draft'
# 						tmp = 'devis envoyé'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'sent'
# 						tmp = 'bon de commande'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'sale'
# 						tmp = 'terminée'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'done'
# 						tmp = 'annulée'
# 						if tmp.find(search.lower()) != -1:
# 							search = 'cancel'
# 						search_domain = OR([search_domain, [('state', 'ilike', search)]])
# 					if search_in in ('amount_total'):
# 						search_domain = OR([search_domain, [('amount_total', 'ilike', search)]])
# 					domain += search_domain
#
# 				# archive_groups = self._get_archive_groups('sale.order', domain)
# 				# if date_begin and date_end:
# 				#    domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
#
# 				# count for pager
# 				orders_count = SaleOrder.search_count(domain)
#
# 				# pager
# 				pager = portal_pager(
# 					url="/my/requests",
# 					url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
# 					total=orders_count,
# 					page=page,
# 					step=self._items_per_page
# 				)
# 				# content according to pager and archive selected
#
# 				orders = SaleOrder.sudo().search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
# 				request.session['my_requests_history'] = orders.ids[:100]
#
# 				# request.env.cr.execute("SELECT id FROM sale_order WHERE state = 'draft'", [])
# 				# orders = request.env.cr.fetchall()
#
# 				values.update({
# 					'date': date_begin,
# 					'orders': orders.sudo(),
# 					'partner': partner,
# 					'page_name': 'requests',
# 					'pager': pager,
# 					# 'archive_groups': archive_groups,
# 					'default_url': '/my/requests',
# 					'searchbar_sortings': searchbar_sortings,
# 					'sortby': sortby,
# 					'searchbar_inputs': searchbar_inputs,
# 					'search_in': search_in,
# 					'search': '',
# 				})
# 				return request.render("certification.portal_my_requests", values)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# SAVE AUDIT REQUESTS
# 	@http.route(['/my/equipments/request'], type='http', auth='user', website=True)
# 	def portal_my_equipments_request(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				equipments = request.httprequest.form.getlist('equipments')
#
# 				saleOrder = request.env['sale.order']
# 				done = request.env['sale.order'].browse()
# 				now = datetime.datetime.now()
# 				template = {
# 					'state': 'draft',
# 					'date_order': now.strftime("%Y-%m-%d %H:%M:%S"),
# 					'user_id': request.env.user.id,
# 					'partner_id': request.env.user.partner_id.id,
# 					# 'partner_invoice_id': request.env.user.partner_id.id,
# 					# 'partner_shipping_id': request.env.user.partner_id.id,
# 				}
#
# 				newSaleOrder = saleOrder.sudo().create(template)
# 				done += newSaleOrder
#
# 				# IF saleOrder created
# 				if done:
# 					for equipment_id in equipments:
# 						# equipment = request.env['critt.equipment'].sudo().search([('id', '=', equipment_id)])
# 						equipment = request.env['critt.equipment'].sudo().browse(int(equipment_id))
# 						if equipment:
# 							template = {
# 								'statut': 'en_cours'
# 							}
# 							equipment.sudo().write(template)
# 							# audit_a_faire => en_cours
# 							saleOrderLineEquipment = request.env['critt.sale.order.line.equipment']
# 							done = request.env['critt.sale.order.line.equipment'].browse()
# 							template = {
# 								'order_id': newSaleOrder.id,
# 								'equipment_id': equipment_id
# 							}
# 							newSaleOrderLineEquipment = saleOrderLineEquipment.sudo().create(template)
# 							done += newSaleOrderLineEquipment
#
# 				return request.render("certification.portal_my_equipments_request", {
# 					'equipments': equipments,
# 					'done': done,
# 					'newAudit': False
# 				})
# 				# return request.redirect('/my/equipments/request')
#
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# FORM AUDIT REQUEST
# 	@route(['/my', '/my/request/<int:request_id>'], type='http', auth="user", website=True)
# 	def portal_my_request(self, request_id, **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				SaleOrder = request.env['sale.order']
#
# 				saleorder = request.env['sale.order'].search([('id', '=', request_id)])
# 				#categories = request.env['critt.equipment.category'].sudo().search([])
#
# 				return request.render("certification.portal_my_request",
# 									  {
# 										  'order': saleorder
# 									  })
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# VALIDATE AUDIT REQUEST
# 	@http.route(['/my/requests/validate'], type='http', auth='user', website=True)
# 	def portal_my_requests_validate(self, **post):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				orders = request.httprequest.form.getlist('ordersSelected')
#
# 				done = False
# 				now = datetime.datetime.now()
# 				for order_id in orders:
# 					saleOrder = request.env['sale.order'].sudo().browse(int(order_id))
# 					if saleOrder:
# 						template = {
# 							'state': 'sale',
# 							'confirmation_date': now.strftime("%Y-%m-%d %H:%M:%S"),
# 							'invoice_status': 'to invoice', #'invoiced'
# 						}
# 						done = saleOrder.sudo().write(template)
#
# 				return request.redirect('/my/equipments')
# 				# return request.redirect('/my/equipments/request')
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# CREATE ATTACHMENT bon de commande pour devis par le client
# 	def _createAttachmentBonDeCommande(self, fileUpload, order):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
#
# 				#remove previous attachment
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM ir_attachment WHERE res_model = 'sale.order' AND res_id = %s AND description = 'Bon de commande client'",
# 					(order.id,))
# 				attachement_ids = [x[0] for x in request.env.cr.fetchall()]
# 				for attachement_id in attachement_ids:
# 					attachmentToDelete = request.env['ir.attachment'].browse(int(attachement_id))
# 					attachmentToDelete.sudo().unlink()
#
# 				now = datetime.datetime.now()
#
# 				Attachments = request.env['ir.attachment']
# 				attachment = fileUpload.read()
# 				template = {
# 					'name': fileUpload.filename,
# 					'res_field': '',
# 					#'datas_fname': fileUpload.filename,  # 'image small.png',
# 					'res_name': fileUpload.filename,
# 					'type': 'binary',
# 					'res_model': 'sale.order',
# 					'res_id': order.id,
# 					'datas': base64.encodestring(attachment),
# 					'checksum': '',
# 					'description': 'Bon de commande client',
# 				}
#
# 				attachment_id = Attachments.sudo().create(template)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	#CREATE ATTACHMENT FOR EQUIPMENT
# 	def _createAttachment(self, file, type, description, equipment_id):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				if type == 'creation':
# 					sequence_certificat = 1
# 				if type == 'controle':
# 					sequence_certificat = 2
# 				if type == 'reforme':
# 					sequence_certificat = 3
# 				now = datetime.datetime.now()
# 				#create critt_certification_certificat
# 				certificat = request.env['critt.certification.certificat']
# 				templateCertificat = {
# 					'desc': description,
# 					'type': type,
# 					'sequence': sequence_certificat,
# 					'id_equipment': equipment_id,
# 					'date': now.strftime("%Y-%m-%d"),
# 					#'dl_pdf': 'critt.equipment' "/web/content/%s?download=1" % attachement_id
# 				}
# 				certificat = certificat.sudo().create(templateCertificat)
#
# 				Attachments = request.env['ir.attachment']
# 				attachment = file.read()
# 				# try:
# 				#    certificat_date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
# 				# except:
# 				#    certificat_date = None
#
# 				template = {
# 					'name': file.filename,
# 					'res_field': '',
# 					#'datas_fname': file.filename,  # 'image small.png',
# 					'res_name': file.filename,
# 					'type': 'binary',
# 					'res_model': 'critt.certification.certificat',
# 					'res_id': certificat.id,
# 					'datas': base64.encodestring(attachment),
# 					'checksum': '',
# 					'description': description,
# 					'type_certificat': type,
# 					'sequence_certificat': sequence_certificat
# 					# 'orga_certif': orga_certif,
# 					# 'certificat_date': certificat_date
# 					# 'file_size': len(base64.encodestring(attachment)),
# 					# attachment.encode('base64'),
# 				}
#
# 				attachment_id = Attachments.sudo().create(template)
#
# 				templateUpdateCertificat = {
# 					'dl_pdf': "/web/content/%s?download=1" % attachment_id.id
# 				}
# 				certificat.sudo().write(templateUpdateCertificat)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
#
# 	def _createAttachmentOld(self, file, type, description, equipment_id):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				Attachments = request.env['ir.attachment']
# 				attachment = file.read()
# 				# try:
# 				#    certificat_date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
# 				# except:
# 				#    certificat_date = None
# 				if type == 'creation':
# 					sequence_certificat = 1
# 				if type == 'control':
# 					sequence_certificat = 2
# 				if type == 'reforme':
# 					sequence_certificat = 3
#
# 				template = {
# 					'name': file.filename,
# 					'res_field': '',
# 					#'datas_fname': file.filename,  # 'image small.png',
# 					'res_name': file.filename,
# 					'type': 'binary',
# 					'res_model': 'critt.equipment',
# 					'res_id': equipment_id,
# 					'datas': base64.encodestring(attachment),
# 					'checksum': '',
# 					'description': description,
# 					'type_certificat': type,
# 					'sequence_certificat': sequence_certificat
# 					# 'orga_certif': orga_certif,
# 					# 'certificat_date': certificat_date
# 					# 'file_size': len(base64.encodestring(attachment)),
# 					# attachment.encode('base64'),
# 				}
#
# 				attachment_id = Attachments.sudo().create(template)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# REMOVE photo equipment
# 	def _remove_equipment_image(self, request, equipment):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				# remove ir.attachement image
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM ir_attachment WHERE name IN ('image', 'image_medium', 'image_small') AND res_model = 'critt.equipment' AND res_id = %s",
# 					(equipment.id,))
# 				attachement_ids = [x[0] for x in request.env.cr.fetchall()]
# 				for attachement_id in attachement_ids:
# 					attachmentToDelete = request.env['ir.attachment'].browse(int(attachement_id))
# 					attachmentToDelete.sudo().unlink()
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# CREATE ATTACHMENT FOR EQUIPMENT
# 	def _set_equipment_image(self, request, file, equipment):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				try:
# 					#remove ir.attachement image
# 					request.env.cr.execute(
# 						"SELECT DISTINCT id FROM ir_attachment WHERE name IN ('image', 'image_medium', 'image_small') AND res_model = 'critt.equipment' AND res_id = %s",
# 						(equipment.id,))
# 					attachement_ids = [x[0] for x in request.env.cr.fetchall()]
# 					for attachement_id in attachement_ids:
# 						attachmentToDelete = request.env['ir.attachment'].browse(int(attachement_id))
# 						attachmentToDelete.sudo().unlink()
#
# 					Attachments = request.env['ir.attachment']
# 					attachment = file.read()
#
# 					template = {
# 					'name': 'image',
# 					'res_name': equipment.name,
# 					'res_model': 'critt.equipment',
# 					'res_field': 'image',
# 					'res_id': equipment.id,
# 					'type': 'binary',
# 					#'datas_fname': file.filename,  # 'image small.png',
# 					'datas': base64.encodestring(attachment),
# 					'checksum': ''
# 					}
# 					attachment_image_id = Attachments.sudo().create(template)
# 					template = {
# 						'name': 'image_medium',
# 						'res_name': equipment.name,
# 						'res_model': 'critt.equipment',
# 						'res_field': 'image_medium',
# 						'res_id': equipment.id,
# 						'type': 'binary',
# 						#'datas_fname': file.filename,  # 'image small.png',
# 						'datas': base64.encodestring(attachment),
# 						'checksum': ''
# 					}
# 					attachment_image_medium_id = Attachments.sudo().create(template)
# 					# template = {
# 					# 	'name': 'image_small',
# 					# 	'res_name': equipment.name,
# 					# 	'res_model': 'critt.equipment',
# 					# 	'res_field': 'image_small',
# 					# 	'res_id': equipment.id,
# 					# 	'type': 'binary',
# 					# 	'datas_fname': file.filename,  # 'image small.png',
# 					# 	'datas': base64.encodestring(attachment),
# 					# 	'checksum': ''
# 					# }
# 					# attachment_image_medium_id = Attachments.sudo().create(template)
# 				except:
# 					error = 'error create photo'
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
#
# 	# REMOVE photo partner
# 	def _remove_partner_image(self, request, partner):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				# remove ir.attachement image
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM ir_attachment WHERE name IN ('image', 'image_medium', 'image_small') AND res_model = 'res.partner' AND res_id = %s",
# 					(partner.id,))
# 				attachement_ids = [x[0] for x in request.env.cr.fetchall()]
# 				for attachement_id in attachement_ids:
# 					attachmentToDelete = request.env['ir.attachment'].browse(int(attachement_id))
# 					attachmentToDelete.sudo().unlink()
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# CREATE ATTACHMENT FOR PARTNER
# 	def _set_partner_image(self, request, file, partner):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group('certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				# remove ir.attachement image
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM ir_attachment WHERE name IN ('image', 'image_medium', 'image_small') AND res_model = 'res.partner' AND res_id = %s",
# 					(partner.id,))
# 				attachement_ids = [x[0] for x in request.env.cr.fetchall()]
# 				for attachement_id in attachement_ids:
# 					attachmentToDelete = request.env['ir.attachment'].browse(int(attachement_id))
# 					attachmentToDelete.sudo().unlink()
#
# 				Attachments = request.env['ir.attachment']
# 				attachment = file.read()
#
# 				template = {
# 					'name': 'image',
# 					'res_name': partner.name,
# 					'res_model': 'res.partner',
# 					'res_field': 'image',
# 					'res_id': partner.id,
# 					'type': 'binary',
# 					#'datas_fname': file.filename,  # 'image small.png',
# 					'datas': base64.encodestring(attachment),
# 					'checksum': ''
# 				}
# 				attachment_image_id = Attachments.sudo().create(template)
# 				template = {
# 					'name': 'image_medium',
# 					'res_name': partner.name,
# 					'res_model': 'res.partner',
# 					'res_field': 'image_medium',
# 					'res_id': partner.id,
# 					'type': 'binary',
# 					#'datas_fname': file.filename,  # 'image small.png',
# 					'datas': base64.encodestring(attachment),
# 					'checksum': ''
# 				}
# 				attachment__image_medium_id = Attachments.sudo().create(template)
# 				template = {
# 					'name': 'image_small',
# 					'res_name': partner.name,
# 					'res_model': 'res.partner',
# 					'res_field': 'image_small',
# 					'res_id': partner.id,
# 					'type': 'binary',
# 					#'datas_fname': file.filename,  # 'image small.png',
# 					'datas': base64.encodestring(attachment),
# 					'checksum': ''
# 				}
# 				attachment__image_medium_id = Attachments.sudo().create(template)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
#
# 	# résultats de recherche
# 	@http.route(['/my/equipments_old', '/my/equipments_old/page/<int:page>'], type='http', auth="user",
# 				website=True)
# 	def portal_my_equipments_old(self, page=1, date_begin=None, date_end=None, search_qr_code='', sortby=None,
# 								 search=None, search_in='all', **kw):  # , search_nfc=''
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group(
# 				'certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				if request.env.user.gest_materiel == False:
# 					return request.redirect('/')
#
# 				values = self._prepare_portal_layout_values_equipments()
# 				partner = request.env.user.partner_id
# 				Equipment = request.env['critt.equipment']
#
# 				# domain = [('active', '=', True), ('owner_user_id', '=', request.env.user.id)]
#
# 				search_qr_code_result = -1
# 				if len(search_qr_code) > 0:
# 					search_qr_code_result = 1
# 					equipments = request.env['critt.equipment'].search(
# 						[('num_materiel', '=', search_qr_code), ('owner_user_id', '=', request.env.user.id)])
# 					if len(equipments) == 1:
# 						Horodating = request.env['critt.horodating']
#
# 						vals = {'user': request.env.user.id, 'action': "Recherche QR Code",
# 								'equipment_id': equipments[0].id}
#
# 						Horodating.create(vals)
#
# 						return request.redirect('/my/equipment/%s' % (equipments[0].id))
#
# 				searchbar_sortings = {
# 					# 'company_name': {'label': _('Client'), 'equipment.partner_id': 'company_name'},
# 					# 'referent': {'label': _('Référent'), 'equipment.partner_id': 'referent'},
# 					'num_materiel': {'label': _('N° de matériel'), 'equipment': 'num_materiel'},
# 					'category_id': {'label': _('Type'), 'equipment': 'category_id'},
# 					'internal_no': {'label': _('N° interne'), 'equipment': 'internal_no'},
# 					'agence': {'label': _('Agence / secteur'), 'equipment': 'agence'},
# 					'equipe': {'label': _('Équipe'), 'equipment': 'equipe'}
# 					# 'audit_suivant': {'label': _('Date prochain contrôle'), 'equipment': 'audit_suivant'},
# 					# 'orga_certif': {'label': _('Organisme de certification'), 'equipment': 'orga_certif'}
# 				}
# 				searchbar_inputs = {
# 					'all': {'input': 'all', 'label': _('Tout')},
# 					# 'company_name': {'input': 'company_name', 'label': _('Client')},
# 					# 'referent': {'input': 'referent', 'label': _('Référent')},
# 					# 'num_materiel': {'input': 'num_materiel', 'label': _('N° de matériel')},
# 					# 'category_id': {'input': 'category_id', 'label': _('Type')},
# 					# 'internal_no': {'input': 'internal_no', 'label': _('N° interne')},
# 					# 'agence': {'input': 'agence', 'label': _('Agence / secteur')},
# 					# 'equipe': {'input': 'equipe', 'label': _('Équipe')}
# 					# 'audit_suivant': {'input': 'audit_suivant', 'label': _('Date prochain contrôle')},
# 					# 'orga_certif': {'input': 'orga_certif', 'label': _('Organisme de certification')}
# 					# 'message': {'input': 'message', 'label': _('Search in Messages')},
# 					# 'customer': {'input': 'customer', 'label': _('Search in Customer')},
#
# 				}
# 				# default sortby order
# 				sort_string = ''
# 				if not sortby:
# 					sort_string = ' ORDER BY e.num_materiel'
# 					sortby = 'num_materiel'
# 				else:
# 					if sortby in ('company_name'):
# 						sort_string = ' ORDER BY p.company_name'
# 					# if sortby in ('referent'):
# 					#	sort_string = ' ORDER BY p.referent'
# 					if sortby in ('num_materiel'):
# 						sort_string = ' ORDER BY e.num_materiel'
# 					if sortby in ('category_id'):
# 						sort_string = ' ORDER BY c.name'
# 					if sortby in ('internal_no'):
# 						sort_string = ' ORDER BY e.internal_no'
# 					if sortby in ('agence'):
# 						sort_string = ' ORDER BY e.agence'
# 					if sortby in ('equipe'):
# 						sort_string = ' ORDER BY e.equipe'
# 				# if sortby in ('audit_suivant'):
# 				#	sort_string = ' ORDER BY e.audit_suivant'
# 				# if sortby in ('orga_certif'):
# 				#	sort_string = ' ORDER BY e.orga_certif'
#
# 				# sort_equipment = searchbar_sortings[sortby]['equipment']
#
# 				# search
# 				request_string = ''
# 				if search and search_in:
# 					search_domain = []
# 					if search_in in ('all'):
# 						request_string = " AND ("
# 						# request_string += " LOWER(p.company_name) like '%" + search.lower() + "%'"
# 						# request_string += " OR LOWER(p.referent) like '%" + search.lower() + "%'"
# 						request_string += "LOWER(e.num_materiel) like '%" + search.lower() + "%'"
# 						request_string += " OR LOWER(c.name) like '%" + search.lower() + "%'"
# 						# request_string += " OR LOWER(c.orga_certif) like '%" + search.lower() + "%'"
# 						# try:
# 						#	date_audit = search.replace('%2F', '/')
# 						#	d = datetime.datetime.strptime(date_audit, '%d/%m/%Y').date()
# 						#	request_string += " OR (e.audit_suivant >= '" + d.strftime("%Y-%m-%d") + " 00:00:00' AND e.audit_suivant <= '" + d.strftime("%Y-%m-%d") + " 23:59:59')"
# 						# except:
# 						#	error = 'error search date audit'
# 						request_string += " OR LOWER(e.internal_no) like '%" + search.lower() + "%'"
# 						request_string += " OR LOWER(e.agence) like '%" + search.lower() + "%'"
# 						request_string += " OR LOWER(e.equipe) like '%" + search.lower() + "%'"
# 						request_string += " )"
#
# 					# request_string = " AND (";
# 					# request_string += " LOWER(p.company_name) like '%" + search.lower() + "%'"
# 					# request_string += " OR LOWER(p.referent) like '%" + search.lower() + "%'"
# 					# request_string += " OR LOWER(e.num_materiel) like '%" + search.lower() + "%'"
# 					# request_string += " OR LOWER(c.name) like '%" + search.lower() + "%'"
# 					# request_string += " OR LOWER(e.audit_suivant) like '%" + search.lower() + "%'"
# 					# request_string += " )"
# 					# search_domain = OR(
# 					#	[search_domain, ['|', '|', '|', '|', ('company_name', 'ilike', search), ('referent', 'ilike', search),
# 					#					 ('num_materiel', 'ilike', search), ('category_id', 'ilike', search),
# 					#					 ('audit_suivant', 'ilike', search)]])
#
# 					# search_domain = OR([search_domain, ['|', '|', '|', '|', '|', '|', ('name', 'ilike', search), ('serial_no', 'ilike', search),
# 					#                                    ('internal_no', 'ilike', search), ('localisation_description', 'ilike', search)
# 					#                                    ('category_id', 'ilike', search), ('statut', 'ilike', search),
# 					#                                    ('orga_certif', 'ilike', search)]])
# 					if search_in in ('company_name'):
# 						# search_domain = OR([search_domain, [('company_name', 'ilike', search)]])
# 						request_string = " AND LOWER(p.company_name) like '%" + search.lower() + "%'"
# 					if search_in in ('referent'):
# 						# search_domain = OR([search_domain, [('referent', 'ilike', search)]])
# 						request_string = " AND LOWER(p.referent) like '%" + search.lower() + "%'"
# 					if search_in in ('num_materiel'):
# 						# search_domain = OR([search_domain, [('num_materiel', 'ilike', search)]])
# 						request_string = " AND LOWER(e.num_materiel) like '%" + search.lower() + "%'"
# 					if search_in in ('category_id'):
# 						# search_domain = OR([search_domain, [('category_id', 'ilike', search)]])
# 						request_string = " AND LOWER(c.name) like '%" + search.lower() + "%'"
# 					# request_string = " AND LOWER(c.name) like '%" + search.lower() + "%'"
# 					if search_in in ('internal_no'):
# 						request_string = " AND LOWER(e.internal_no) like '%" + search.lower() + "%'"
# 					if search_in in ('agence'):
# 						request_string = " AND LOWER(e.agence) like '%" + search.lower() + "%'"
# 					if search_in in ('equipe'):
# 						request_string = " AND LOWER(e.equipe) like '%" + search.lower() + "%'"
# 					if search_in in ('audit_suivant'):
# 						# search_domain = OR([search_domain, [('audit_suivant', 'ilike', search)]])
# 						try:
# 							date_audit = search.replace('%2F', '/')
# 							d = datetime.datetime.strptime(date_audit, '%d/%m/%Y').date()
# 							# request_string += " OR LOWER(e.audit_suivant) like '%" + d.strftime("%Y-%m-%d") + "%'"
# 							request_string += " AND (e.audit_suivant >= '" + d.strftime(
# 								"%Y-%m-%d") + " 00:00:00' AND e.audit_suivant <= '" + d.strftime(
# 								"%Y-%m-%d") + " 23:59:59')"
# 						except:
# 							error = 'error search date audit'
# 					if search_in in ('orga_certif'):
# 						# search_domain = OR([search_domain, [('num_materiel', 'ilike', search)]])
# 						request_string = " AND LOWER(e.orga_certif) like '%" + search.lower() + "%'"
#
# 				# if search_in in ('customer', 'all'):
# 				#    search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
# 				# if search_in in ('message', 'all'):
# 				#    search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
#
# 				# archive_groups = self._get_archive_groups('sale.order', domain)
# 				# if date_begin and date_end:
# 				#    domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
#
# 				request_string = """SELECT e.id FROM critt_equipment as e
# 								LEFT JOIN critt_equipment_category as c ON e.category_id = c.id
# 								JOIN res_users as u ON e.owner_user_id = u.id
# 								JOIN public.res_partner as p ON u.partner_id = p.id
# 							   WHERE e.active = true AND e.owner_user_id =
# 						   """ + str(request.env.user.id) + request_string + sort_string
#
# 				request.env.cr.execute(request_string)
# 				equipments_ids = [x[0] for x in request.env.cr.fetchall()]
# 				equipments_count = len(equipments_ids)
# 				if page:
# 					request_string += " LIMIT " + str(self._items_per_page)
#
# 				request.env.cr.execute(request_string)
# 				equipments_ids = [x[0] for x in request.env.cr.fetchall()]
# 				equipments = request.env['critt.equipment'].sudo().browse(equipments_ids)
#
# 				# count for pager
# 				# equipments = Equipment.search(domain, order=sort_equipment, limit=self._items_per_page)
# 				# equipments_count = Equipment.search_count(domain)
#
# 				# if search_in == 'date_last_audit':
# 				#	tmp = 0
# 				#	for equipment in equipments:
# 				#		if search in equipment.date_last_audit_string:  # and search in equipment.date_last_audit_string)
# 				#			tmp += 1
# 				#	equipments_count = tmp
#
# 				# pager
# 				if search:
# 					url_args = {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,
# 								'search_in': search_in,
# 								'search': search}
# 				else:
# 					url_args = {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby}
#
# 				pager = portal_pager(
# 					url="/my/equipments",
# 					url_args=url_args,
# 					total=equipments_count,
# 					page=page,
# 					step=self._items_per_page
# 				)
# 				# content according to pager and archive selected
# 				# equipments = Equipment.search(domain, order=sort_equipment, limit=self._items_per_page, offset=pager['offset'])
# 				if page:
# 					request_string += " OFFSET " + str(page - 1)
# 				request.env.cr.execute(request_string)
# 				equipments_ids = [x[0] for x in request.env.cr.fetchall()]
# 				equipments = request.env['critt.equipment'].sudo().browse(equipments_ids)
# 				request.session['my_equipments_history'] = equipments.ids[:100]
#
# 				request.env.cr.execute(
# 					"SELECT DISTINCT id FROM res_partner "
# 					"WHERE parent_id = %s",
# 					(partner.id,))
# 				ids = [x[0] for x in request.env.cr.fetchall()]
# 				referents = request.env['res.partner'].sudo().browse(ids)
#
# 				# search_nfc_result = -1
# 				# if len(search_nfc) > 0:
# 				# 	search_nfc_result = 1
# 				# 	equipments = request.env['critt.equipment'].search(
# 				# 		[('nfc', '=', search_nfc), ('owner_user_id', '=', request.env.user.id)])
# 				# 	if len(equipments) == 1:
# 				# 		return request.redirect('/my/equipment/%s' % (equipments[0].id))
#
# 				if len(search_qr_code) > 0:
# 					equipments = None
# 				else:
# 					equipments = equipments.sudo()
#
# 				values.update({
# 					'referents': referents,
# 					'count': equipments_count,
# 					'date': date_begin,
# 					'equipments': equipments,
# 					'partner': partner,
# 					'page_name': 'equipments',
# 					'pager': pager,
# 					'page': page,
# 					# 'archive_groups': archive_groups,
# 					'default_url': '/my/equipments',
# 					'searchbar_sortings': searchbar_sortings,
# 					'sortby': sortby,
# 					'searchbar_inputs': searchbar_inputs,
# 					'search_in': search_in,
# 					'search': search,
# 					'request_string': request_string,
# 					'url_args': url_args,
# 					# 'search_nfc': search_nfc,
# 					# 'search_nfc_result': search_nfc_result,
# 					'search_qr_code': search_qr_code,
# 					'search_qr_code_result': search_qr_code_result,
# 				})
# 				return request.render("certification.equipments", values)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
#
# 	# LIST EQUIPMENTS (OLD)
# 	@http.route(['/my/equipments2', '/my/equipments/page/<int:page>'], type='http', auth="user", website=True)
# 	def portal_my_equipments2(self, page=1, date_begin=None, date_end=None, sortby=None, search=None,
# 							  search_in='all', **kw):
# 		if request.env.user.has_group('certification.website_lvl_1') or request.env.user.has_group(
# 				'certification.certification_lvl_1'):
# 			if request.env.user.partner_id.date_fin_essai and request.env.user.partner_id.date_fin_essai < datetime.datetime.now().date():
# 				return request.render("certification.essai_depasse")
# 			else:
# 				# if request.env.user.gest_materiel == False:
# 				#	return request.redirect('/')
#
# 				values = self._prepare_portal_layout_values_equipments()
# 				partner = request.env.user.partner_id
# 				Equipment = request.env['critt.equipment']
#
# 				# domain = [
# 				#   ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
# 				#    ('state', 'in', ['sale', 'done'])
# 				# ]
# 				domain = [('active', '=', True), ('owner_user_id', '=', request.env.user.id)]
#
# 				searchbar_sortings = {
# 					'name': {'label': _('Nom'), 'equipment': 'name'},
# 					'num_materiel': {'label': _('N° de matériel'), 'equipment': 'num_materiel'},
# 					'statut': {'label': _('Statut'), 'equipment': 'statut'},
# 					'orga_certif': {'label': _('Organisme certifiant'), 'equipment': 'orga_certif'},
# 					'date_last_audit': {'label': _('Date dernier audit'), 'equipment': 'date_last_audit'}
# 				}
# 				searchbar_inputs = {
# 					'all': {'input': 'all', 'label': _('Tout')},
# 					'name': {'input': 'name', 'label': _('Nom')},
# 					'num_materiel': {'input': 'num_materiel', 'label': _('Numéro de matériel')},
# 					'internal_no': {'input': 'internal_no', 'label': _('Numéro interne')},
# 					'team': {'input': 'team', 'label': _('Équipe')},
# 					'category_id': {'input': 'category_id', 'label': _('Catégorie')},
# 					'statut': {'input': 'statut', 'label': _('Statut')},
# 					'orga_certif': {'input': 'orga_certif', 'label': _('Organisme certifiant')},
# 					'date_last_audit': {'input': 'date_last_audit', 'label': _('Date dernier audit')}
# 					# 'message': {'input': 'message', 'label': _('Search in Messages')},
# 					# 'customer': {'input': 'customer', 'label': _('Search in Customer')},
#
# 				}
# 				# default sortby order
# 				if not sortby:
# 					sortby = 'name'
# 				sort_equipment = searchbar_sortings[sortby]['equipment']
#
# 				# search
# 				# request_string = ''
# 				if search and search_in:
# 					search_domain = []
# 					if search_in in ('all'):
# 						search_domain = OR(
# 							[search_domain,
# 							 ['|', '|', '|', '|', ('name', 'ilike', search), ('num_materiel', 'ilike', search),
# 							  ('category_id', 'ilike', search), ('statut', 'ilike', search),
# 							  ('orga_certif', 'ilike', search)]])
#
# 					# search_domain = OR([search_domain, ['|', '|', '|', '|', '|', '|', ('name', 'ilike', search), ('serial_no', 'ilike', search),
# 					#                                    ('internal_no', 'ilike', search), ('localisation_description', 'ilike', search)
# 					#                                    ('category_id', 'ilike', search), ('statut', 'ilike', search),
# 					#                                    ('orga_certif', 'ilike', search)]])
# 					if search_in in ('name'):
# 						search_domain = OR([search_domain, [('name', 'ilike', search)]])
# 					# request_string = " AND LOWER(e.name) like '%" + search.lower() + "%'"
# 					if search_in in ('num_materiel'):
# 						search_domain = OR([search_domain, [('num_materiel', 'ilike', search)]])
# 					# request_string = " AND LOWER(e.serial_no) like '%" + search.lower() + "%'"
# 					if search_in in ('internal_no'):
# 						search_domain = OR([search_domain, [('internal_no', 'ilike', search)]])
# 					if search_in in ('team'):
# 						search_domain = OR([search_domain, [('localisation_description', 'ilike', search)]])
# 					if search_in in ('category_id'):
# 						search_domain = OR([search_domain, [('category_id', 'ilike', search)]])
# 					# request_string = " AND LOWER(c.name) like '%" + search.lower() + "%'"
# 					if search_in in ('statut'):
# 						search_domain = OR([search_domain, [('statut', 'ilike', search)]])
# 					# request_string = " AND LOWER(e.statut) like '%" + search.lower() + "%'"
# 					if search_in in ('orga_certif'):
# 						search_domain = OR([search_domain, [('orga_certif', 'ilike', search)]])
# 					# request_string = " AND LOWER(e.orga_certif) like '%" + search.lower() + "%'"
# 					# if search_in in ('date_last_audit'):
# 					# request_string = " AND date_last_audit like '%" + search + "%'"
# 					# search_domain = OR([search_domain, [('audits[0].etat_audit', 'ilike', search)]])
# 					# toto = search.replace('%2F', '/')
# 					# d = datetime.datetime.strptime(toto, '%d/%m/%Y').date()
# 					# search_domain = OR([search_domain, [('date_last_audit', '=', d)]])
# 					# search_domain = OR([search_domain, [('last_audit', '=', search)]])
#
# 					domain += search_domain
# 				# if search_in in ('customer', 'all'):
# 				#    search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
# 				# if search_in in ('message', 'all'):
# 				#    search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
#
# 				# archive_groups = self._get_archive_groups('sale.order', domain)
# 				# if date_begin and date_end:
# 				#    domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
#
# 				# request_string = """SELECT e.id FROM critt_equipment as e
# 				#                JOIN critt_equipment_category as c ON e.category_id = c.id
# 				#               WHERE e.active = true AND e.owner_user_id =
# 				#           """ + str(request.env.user.id) + request_string
# 				# request.env.cr.execute(request_string)
# 				# equipments_ids = [x[0] for x in request.env.cr.fetchall()]
# 				# equipments = request.env['critt.equipment'].sudo().browse(equipments_ids)
# 				# equipments_count = len(equipments)
#
# 				# count for pager
# 				equipments = Equipment.search(domain, order=sort_equipment, limit=self._items_per_page)
# 				equipments_count = Equipment.search_count(domain)
#
# 				if search_in == 'date_last_audit':
# 					tmp = 0
# 					for equipment in equipments:
# 						if search in equipment.date_last_audit_string:  # and search in equipment.date_last_audit_string)
# 							tmp += 1
# 					equipments_count = tmp
#
# 				# pager
# 				if search:
# 					url_args = {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,
# 								'search_in': search_in, 'search': search}
# 				else:
# 					url_args = {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby}
# 				pager = portal_pager(
# 					url="/my/equipments",
# 					url_args=url_args,
# 					total=equipments_count,
# 					page=page,
# 					step=self._items_per_page
# 				)
# 				# content according to pager and archive selected
# 				equipments = Equipment.search(domain, order=sort_equipment, limit=self._items_per_page,
# 											  offset=pager['offset'])
#
# 				request.session['my_equipments_history'] = equipments.ids[:100]
#
# 				values.update({
# 					'count': equipments_count,
# 					'date': date_begin,
# 					'equipments': equipments.sudo(),
# 					'partner': partner,
# 					'page_name': 'equipments',
# 					'pager': pager,
# 					'page': page,
# 					# 'archive_groups': archive_groups,
# 					'default_url': '/my/equipments',
# 					'searchbar_sortings': searchbar_sortings,
# 					'sortby': sortby,
# 					'searchbar_inputs': searchbar_inputs,
# 					'search_in': search_in,
# 					'search': search,
# 				})
# 				return request.render("certification.portal_my_equipments", values)
# 		else:
# 			if request.env.user.has_group('certification.website_lvl_0'):
# 				return request.render("certification.subscribe")
# 			else:
# 				return request.render("website.homepage")
