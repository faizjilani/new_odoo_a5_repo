# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _


class TubaSaleDamage(models.Model):
    _name = 'tuba.sale.damage'
    _rec_name = 'reference_no'
    _description = 'Tuba Sale Damage'

    reference_no = fields.Char('Reference Number', default=lambda self: _('New'), required=True, readonly=True)
    new_damage_date = fields.Date("Damage Date", default=datetime.today().date(), required=True)
    damage_reason = fields.Text('Reason')
    tuba_damage_lines = fields.One2many('tuba.sale.damage.lines',
                                        'tuba_sale_damage_line', 'Tuba Damage Lines')

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'tuba.sale.damage') or _('New')
        res = super(TubaSaleDamage, self).create(vals)
        return res


class TubaSaleDamageLines(models.Model):
    _name = 'tuba.sale.damage.lines'
    _description = 'Tuba Sale Damage Lines'

    product_id = fields.Many2one('tuba.products', string="Product", required=True)
    prod_qty = fields.Float(string="Quantity", required=True)
    tuba_sale_damage_line = fields.Many2one('tuba.sale.damage', string="Tuba Sale Damage")
    prod_damage_price = fields.Float(string="Unit Price", required=True)
    tax = fields.Float(string="Tax %", default=0.0)
    sub_total = fields.Float(string="Sub Total")

    # def _compute_sub_total(self):
    #     for i in self:
    #         total = i.prod_qty * i.prod_damage_price
    #         tax = (total * i.tax) / 100
    #         i.sub_total = total + tax
