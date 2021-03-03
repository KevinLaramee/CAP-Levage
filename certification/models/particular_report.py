# Tentaive de création d'un "custom template" en utilisant le tuto odoo https://www.odoo.com/documentation/11.0/reference/reports.html#custom-reports
# Ce code a pour but, à terme, de permettre de modifier plus librement l'en-tête et la signature des certificat (permettrait d'ajouter des champs non présent dans odoo
# Actuellement, ce code génère cette erreur: AttributeError: 'report.certification.report_certificat_conforme' object has no attribute 'get_report_values'
# Pour utiliser les valeurs retournées par ce code, faire appel la variable 'modele_certificat' depuis le template du certificat


# from odoo import api, models, fields
#
# class ModeleCertificat(models.Model):
#     _name = "critt.modele_certificat"
#     _description = "Classe permettant de modifier l'en-tête et la signature du certificat"
#
#     desc = fields.Text(string = "En-tête")
#     logo = fields.Binary(string = "Logo")
#     signature = fields.Text(string = "Signature")
#
# class ParticularReport(models.AbstractModel):
#     _name = "report.certification.report_certificat_conforme"
#     @api.model
#     def render_html(self, docids, data=None):
#         report_obj = self.env['report']
#         report = report_obj._get_report_from_name('certification.report_certificat_conforme')
#         docargs = {
#             'doc_ids': docids,
#             'doc_model': report.model,
#             'docs': self,
#         }
#         modele_certificat = self.env['critt.modele_certificat'].search([('id', '=', 1)], limit=1)
#         if modele_certificat:
#             docargs.update({'modele_certificat': modele_certificat})
#         return report_obj.render('certification.report_certificat_conforme', docargs)
