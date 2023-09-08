# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _


class CustomerReceiving(models.Model):
    _name = 'customer.receiving'
    _rec_name = 'reference_no'
    _description = 'Customer Receiving'

    reference_no = fields.Char('Reference Number', default=lambda self: _('New'), required=True, readonly=True)
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    new_receiving_date = fields.Date("Receipt Date", default=datetime.today().date(), required=True)
    receiving_type = fields.Selection([('cash', 'Cash'), ('bank', 'Bank')], string="Receipt Type", required=True)
    receiving_payment = fields.Monetary('Receipt')
    currency_id = fields.Many2one('res.currency', string="Currency", compute="_compute_currency")
    receipt_description = fields.Text('Description')

    def _compute_currency(self):
        for i in self:
            i.currency_id = i.env.user.company_id.currency_id if i.env.user.company_id.currency_id else False

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'customer.receiving') or _('New')
        res = super(CustomerReceiving, self).create(vals)
        return res




