# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TubaProducts(models.Model):
    _name = 'tuba.products'
    _description = 'Tuba Products'

    name = fields.Char(string="Name")
    unit_qty = fields.Float(string="Remaining Quantity", compute="compute_remaining_qty")
    region = fields.Many2one('res.country', string="Region")
    unit = fields.Selection([('box', 'BOX'), ('bag', 'BAG'), ('ctn', 'CTN'), ('man', 'MAN'), ('kg', 'KG'),
                             ('pkt', 'PKT')], string="Unit", required=True)
    currency_id = fields.Many2one('res.currency', string="Currency", compute="_compute_currency")
    sale_price = fields.Monetary('Sale Price')
    total_purchase = fields.Float("Purchase", compute="compute_total_purchase")
    total_sale = fields.Float("Sale", compute="compute_total_sale")
    sales_count = fields.Integer(compute='compute_sale_count')
    purchase_count = fields.Integer(compute='compute_purchase_count')

    def compute_sale_count(self):
        for record in self:
            record.sales_count = self.env['tuba.sale.order'].search_count(
                [('tuba_order_lines.product_id', '=', self.id)])

    def get_sales(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales',
            'view_mode': 'tree,form',
            'res_model': 'tuba.sale.order',
            'domain': [('tuba_order_lines.product_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def compute_purchase_count(self):
        for record in self:
            record.purchase_count = self.env['tuba.purchase.order'].search_count(
                [('tuba_purchase_lines.product_id', '=', self.id)])

    def get_purchases(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchases',
            'view_mode': 'tree,form',
            'res_model': 'tuba.purchase.order',
            'domain': [('tuba_purchase_lines.product_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def _compute_currency(self):
        for i in self:
            i.currency_id = i.env.user.company_id.currency_id if i.env.user.company_id.currency_id else False

    def compute_total_sale(self):
        for i in self:
            total_sale = 0.0
            sale = self.env['tuba.sale.order.lines'].search([('product_id', '=', i.id)])
            if sale:
                for s in sale:
                    total_sale += s.prod_qty
            i.total_sale = total_sale

    def compute_total_purchase(self):
        for i in self:
            total_purchase = 0.0
            purchase = self.env['tuba.purchase.order.lines'].search([('product_id', '=', i.id)])
            if purchase:
                for p in purchase:
                    total_purchase += p.prod_qty
            i.total_purchase = total_purchase

    def remove_products(self):
        purchase_lines = self.env['tuba.purchase.order.lines'].search([('tuba_purchase_order_line', '=', False)])
        for i in purchase_lines:
            i.unlink()
        sale_lines = self.env['tuba.sale.order.lines'].search([('tuba_sale_order_line', '=', False)])
        for i in sale_lines:
            i.unlink()
        damage_lines = self.env['tuba.sale.damage.lines'].search([('tuba_sale_damage_line', '=', False)])
        for i in damage_lines:
            i.unlink()

    def compute_remaining_qty(self):
        for i in self:
            i.unit_qty = i.total_purchase - i.total_sale
