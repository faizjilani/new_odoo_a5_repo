# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class TubaSaleOrder(models.Model):
    _name = 'tuba.sale.order'
    _rec_name = 'reference_no'
    _description = 'Tuba Sale Orders'

    reference_no = fields.Char('Reference Number', default=lambda self: _('New'), required=True, readonly=True)
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    new_order_date = fields.Date("Order Date", default=datetime.today().date(), required=True)
    tuba_order_lines = fields.One2many('tuba.sale.order.lines',
                                       'tuba_sale_order_line', 'Tuba Order Lines')
    currency_id = fields.Many2one('res.currency', string="Currency", compute="_compute_currency")
    total_amount = fields.Monetary(string="Total Amount", compute="_compute_total_amount")

    def _compute_currency(self):
        for i in self:
            i.currency_id = i.env.user.company_id.currency_id if i.env.user.company_id.currency_id else False

    def _compute_total_amount(self):
        for i in self:
            total = 0.0
            if i.tuba_order_lines:
                for line in i.tuba_order_lines:
                    total += line.sub_total
            i.total_amount = total

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'tuba.sale.order') or _('New')
        res = super(TubaSaleOrder, self).create(vals)
        return res


class TubaSaleOrderLines(models.Model):
    _name = 'tuba.sale.order.lines'
    _description = 'Tuba Sale Order Lines'

    product_id = fields.Many2one('tuba.products', string="Product")
    prod_qty = fields.Float(string="Quantity")
    unit = fields.Selection([('box', 'BOX'), ('bag', 'BAG'), ('ctn', 'CTN'), ('man', 'MAN'), ('kg', 'KG'),
                             ('pkt', 'PKT')], string="Unit Type", required=True)
    prod_sale_price = fields.Float(string="Unit Price")
    tax = fields.Float(string="Tax %", default=0.0)
    sub_total = fields.Float(string="Sub Total", compute="_compute_sub_total")
    remain_qty = fields.Float('Remaining Qty', related='product_id.unit_qty', tracking=True)
    tuba_sale_order_line = fields.Many2one('tuba.sale.order', string="Tuba Sale Order")

    def _compute_sub_total(self):
        for i in self:
            total = i.prod_qty * i.prod_sale_price
            tax = (total * i.tax) / 100
            i.sub_total = total + tax

    @api.onchange("product_id")
    def sale_price(self):
        for i in self:
            if i.product_id:
                i.unit = i.product_id.unit

    @api.onchange("prod_qty")
    def check_qty(self):
        for i in self:
            if i.product_id:
                qty = i.remain_qty - i.prod_qty
                if qty < 0.0:
                    raise AccessError(_(f"{i.product_id.name} is Out of Stock!"))

    @api.constrains("prod_qty")
    def check_remain_qty(self):
        for i in self:
            if i.product_id:
                qty = i.remain_qty - i.prod_qty
                if qty < 0.0:
                    raise AccessError(_(f"{i.product_id.name} is Out of Stock!"))
