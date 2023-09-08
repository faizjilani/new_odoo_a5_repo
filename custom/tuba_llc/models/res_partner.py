# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    emirates_id = fields.Char("Emirates ID")
    opening_balance = fields.Float("Customer Opening Balance")
    supplier_opening_balance = fields.Float("Supplier Opening Balance")

    customer_purchase_count = fields.Integer(compute='compute_purchase_count')
    customer_sale_count = fields.Integer(compute='compute_sale_count')

    last_receiving = fields.Date("Last Receiving", compute="compute_receiving")
    customer_type = fields.Selection([('individual', 'Individual'), ('company', 'Company')],
                                     'Customer Type', default="individual")

    def compute_receiving(self):
        for i in self:
            last_date = []
            last = self.env['customer.receiving'].search([('customer_id', '=', i.id)])
            if last:
                for new in last:
                    last_date.append(new.new_receiving_date)
                i.last_receiving = max(last_date) if last_date else False
            else:
                i.last_receiving = False

    def compute_purchase_count(self):
        for record in self:
            record.customer_purchase_count = self.env['tuba.purchase.order'].search_count(
                [('customer_id', '=', self.id)])

    def get_purchases(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchases',
            'view_mode': 'tree,form',
            'res_model': 'tuba.purchase.order',
            'domain': [('customer_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def compute_sale_count(self):
        for record in self:
            record.customer_sale_count = self.env['tuba.sale.order'].search_count(
                [('customer_id', '=', self.id)])

    def get_sales(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales',
            'view_mode': 'tree,form',
            'res_model': 'tuba.sale.order',
            'domain': [('customer_id', '=', self.id)],
            'context': "{'create': False}"
        }
