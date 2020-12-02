from odoo import api, fields, models, _


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        res = super(AccountInvoiceInherit, self).create(vals)

        sale_order = self.env['sale.order'].search([('name', '=', res.invoice_origin)])
        if sale_order:
            for equipment in sale_order.order_line_equipment:
                equipment.equipment_id.write({'derniere_facture': res.id, 'num_derniere_facture': res.name})

        return res

    def write(self, vals):
        res = super(AccountInvoiceInherit, self).write(vals)

        for record in self:
            sale_order = self.env['sale.order'].search([('name', '=', record.invoice_origin)])
            if sale_order:
                for equipment in sale_order.order_line_equipment:
                    equipment.equipment_id.write({'derniere_facture': record.id, 'num_derniere_facture': record.name})

        return res
