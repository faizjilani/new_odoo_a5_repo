# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _


class SupplierPayment(models.Model):
    _name = 'supplier.payment'
    _rec_name = 'reference_no'
    _description = 'Supplier Payment'

    reference_no = fields.Char('Reference Number', default=lambda self: _('New'), required=True, readonly=True)
    customer_id = fields.Many2one('res.partner', string="Supplier", required=True)
    new_payment_date = fields.Date("Payment Date", default=datetime.today().date(), required=True)
    payment_type = fields.Selection([('cash', 'Cash'), ('bank', 'Bank')], string="Payment Type", required=True)
    payment = fields.Monetary('Payment')
    currency_id = fields.Many2one('res.currency', string="Currency", compute="_compute_currency")
    payment_description = fields.Text('Description')

    def _compute_currency(self):
        for i in self:
            i.currency_id = i.env.user.company_id.currency_id if i.env.user.company_id.currency_id else False

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'supplier.payment') or _('New')
        res = super(SupplierPayment, self).create(vals)
        return res




