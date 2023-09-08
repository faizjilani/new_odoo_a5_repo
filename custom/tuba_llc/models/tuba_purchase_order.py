# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _


class TubaPurchaseOrder(models.Model):
    _name = 'tuba.purchase.order'
    _rec_name = 'reference_no'
    _description = 'Tuba Purchase Orders'

    reference_no = fields.Char('Reference Number', default=lambda self: _('New'), required=True, readonly=True)
    customer_id = fields.Many2one('res.partner', string="Supplier", required=True)
    new_order_date = fields.Date("Order Date", default=datetime.today().date(), required=True)
    tuba_purchase_lines = fields.One2many('tuba.purchase.order.lines',
                                          'tuba_purchase_order_line', 'Tuba Order Lines')
    currency_id = fields.Many2one('res.currency', string="Currency", compute="_compute_currency")
    total_amount = fields.Monetary(string="Total Amount", compute="_compute_total_amount")

    def _compute_currency(self):
        for i in self:
            i.currency_id = i.env.user.company_id.currency_id if i.env.user.company_id.currency_id else False

    def _compute_total_amount(self):
        for i in self:
            total = 0.0
            if i.tuba_purchase_lines:
                for line in i.tuba_purchase_lines:
                    total += line.sub_total
            i.total_amount = total

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'tuba.purchase.order') or _('New')
        res = super(TubaPurchaseOrder, self).create(vals)
        return res


class TubaPurchaseOrderLines(models.Model):
    _name = 'tuba.purchase.order.lines'
    _description = 'Tuba Purchase Order Lines'

    product_id = fields.Many2one('tuba.products', string="Product")
    prod_qty = fields.Float(string="Quantity")
    unit = fields.Selection([('box', 'BOX'), ('bag', 'BAG'), ('ctn', 'CTN'), ('man', 'MAN'), ('kg', 'KG'),
                             ('pkt', 'PKT')], string="Unit Type", required=True)
    prod_purchase_price = fields.Float(string="Unit Price")
    tax = fields.Float(string="Tax %", default=0.0)
    sub_total = fields.Float(string="Sub Total", compute="_compute_sub_total")
    tuba_purchase_order_line = fields.Many2one('tuba.purchase.order', string="Tuba Purchase Order")

    def _compute_sub_total(self):
        for i in self:
            total = i.prod_qty * i.prod_purchase_price
            tax = (total * i.tax) / 100
            i.sub_total = total + tax

    @api.onchange("product_id")
    def purchase_sale_price(self):
        for i in self:
            if i.product_id:
                i.prod_purchase_price = i.product_id.sale_price
                i.unit = i.product_id.unit

    @api.onchange("sub_total")
    def purchase_unit_calculate_on_sub_total(self):
        for i in self:
            if i.product_id:
                prod_purchase_price = i.sub_total / i.prod_qty
                i.prod_purchase_price = prod_purchase_price
