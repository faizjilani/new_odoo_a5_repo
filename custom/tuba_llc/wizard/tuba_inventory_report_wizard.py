import logging

# from statistics import mean
from odoo import models, fields, _
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class TubaInventoryReport(models.TransientModel):
    _name = 'tuba.inventory.report.wizard'

    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)

    def check_report(self):
        total_damage = 0.0
        open_total_value = 0.0
        close_total_value = 0.0
        inward_total_value = 0.0
        outward_total_value = 0.0
        open_total_qty = 0.0
        close_total_qty = 0.0
        inward_total_qty = 0.0
        outward_total_qty = 0.0
        start_date = self.start_date
        end_date = self.end_date
        if start_date > end_date:
            raise AccessError(_("Start Date Must be Less than from End Date!"))
        products = self.env['tuba.products'].search([])
        prev_month_closing = []
        for pro in products:
            # avg_sale_price = []
            # avg_purchase_price = []
            prev_sale_qty = 0.0
            prev_purchase_qty = 0.0
            prev_sale_sub_total = 0.0
            prev_purchase_sub_total = 0.0
            current_month_purchase_qty = 0.0
            current_month_sale_qty = 0.0
            current_sale_sub_total = 0.0
            current_purchase_sub_total = 0.0
            prev_damage_qty = 0.0
            prev_damage_sub_total = 0.0
            current_month_damage_qty = 0.0
            current_month_damage_sub_total = 0.0
            previous_damage_products = self.env['tuba.sale.damage.lines'].search(
                [('tuba_sale_damage_line.new_damage_date', '<', start_date),
                 ('product_id', '=', pro.id)])
            if previous_damage_products:
                for dmg in previous_damage_products:
                    prev_damage_qty += dmg.prod_qty
                    prev_damage_sub_total += dmg.sub_total

            current_damage_products = self.env['tuba.sale.damage.lines'].search(
                [('tuba_sale_damage_line.new_damage_date', '>=', start_date),
                 ('tuba_sale_damage_line.new_damage_date', '<=', end_date),
                 ('product_id', '=', pro.id)])
            if current_damage_products:
                for dmg in current_damage_products:
                    current_month_damage_qty += dmg.prod_qty
                    current_month_damage_sub_total += dmg.sub_total

            previous_purchase = self.env['tuba.purchase.order.lines'].search(
                [('tuba_purchase_order_line.new_order_date', '<', start_date),
                 ('product_id', '=', pro.id)])
            if previous_purchase:
                for purchase in previous_purchase:
                    prev_purchase_qty += purchase.prod_qty
                    prev_purchase_sub_total += purchase.sub_total

            previous_sale = self.env['tuba.sale.order.lines'].search(
                [('tuba_sale_order_line.new_order_date', '<', start_date),
                 ('product_id', '=', pro.id)])

            if previous_sale:
                for sale in previous_sale:
                    prev_sale_qty += sale.prod_qty
                    prev_sale_sub_total += sale.sub_total

            current_month_purchase = self.env['tuba.purchase.order.lines'].search(
                [('tuba_purchase_order_line.new_order_date', '>=', start_date),
                 ('tuba_purchase_order_line.new_order_date', '<=', end_date),
                 ('product_id', '=', pro.id)])

            if current_month_purchase:
                for purchase in current_month_purchase:
                    current_purchase_sub_total += purchase.sub_total
                    current_month_purchase_qty += purchase.prod_qty
                    # avg_purchase_price.append(purchase.prod_purchase_price)

            current_month_sale = self.env['tuba.sale.order.lines'].search(
                [('tuba_sale_order_line.new_order_date', '>=', start_date),
                 ('tuba_sale_order_line.new_order_date', '<=', end_date),
                 ('product_id', '=', pro.id)])

            if current_month_sale:
                for sale in current_month_sale:
                    current_month_sale_qty += sale.prod_qty
                    current_sale_sub_total += sale.sub_total
                    # avg_sale_price.append(sale.prod_sale_price)

            open_blnc_qty = prev_purchase_qty - prev_sale_qty
            inward_qty = current_month_purchase_qty if current_month_purchase_qty != 0 else 0.0
            outward_qty = current_month_sale_qty + prev_damage_qty + current_month_damage_qty \
                if current_month_sale_qty != 0 else 0.0
            close_blnc_qty = (open_blnc_qty + inward_qty) - outward_qty
            inward_rate = current_purchase_sub_total / inward_qty if inward_qty != 0 else 0.0
            outward_rate = current_sale_sub_total / outward_qty if outward_qty != 0 else 0.0
            open_blnc_value = prev_purchase_sub_total - prev_sale_sub_total
            inward_value = inward_qty * inward_rate
            outward_value = outward_qty * outward_rate if outward_rate != 0 else 0.0
            open_blnc_rate = open_blnc_value / open_blnc_qty if open_blnc_qty != 0 else 0.0
            mid_qty = open_blnc_qty + inward_qty
            mid_value = open_blnc_value + inward_value
            cls_value = mid_value / mid_qty if mid_qty != 0 else 0.0
            sale_profit = outward_value - (cls_value * outward_qty)
            close_blnc_value = (open_blnc_value + inward_value + sale_profit) - outward_value
            cls_qty = close_blnc_qty if close_blnc_qty != 0 else 0.0
            close_blnc_rate = close_blnc_value / cls_qty if cls_qty != 0 else 0.0
            if close_blnc_value:
                every_pro_profit_loss = (close_blnc_value + outward_value) - open_blnc_value - inward_value
                total_damage += current_month_damage_qty
                dic = {
                    'name': pro.name,
                    'credit': prev_sale_qty,
                    'debit': prev_purchase_qty,
                    'opening_qty': round(open_blnc_qty, 3) if open_blnc_qty else "",
                    'open_rate': round(open_blnc_rate, 3) if open_blnc_rate else "",
                    'open_value': round(open_blnc_value, 3) if open_blnc_value else "",
                    'inward_qty': round(inward_qty, 3) if inward_qty else "",
                    'inward_rate': round(inward_rate, 3) if inward_rate else "",
                    'inward_value': round(inward_value, 3) if inward_value else "",
                    'outward_qty': round(outward_qty, 3) if outward_qty else "",
                    'outward_rate': round(outward_rate, 3) if outward_rate else "",
                    'outward_value': round(outward_value, 3) if outward_rate else "",
                    'close_qty': round(close_blnc_qty, 3) if close_blnc_qty else "",
                    'close_rate': round(close_blnc_rate, 3) if close_blnc_rate else "",
                    'close_value': round(close_blnc_value, 3) if close_blnc_value else "",
                    'damage_products': current_month_damage_qty + prev_damage_qty,
                    'main_profit_loss': round(every_pro_profit_loss, 3),
                    'profit_active': True if every_pro_profit_loss < 0 else False,
                }
                prev_month_closing.append(dic)
            open_total_value += open_blnc_value
            close_total_value += close_blnc_value
            inward_total_value += inward_value
            outward_total_value += outward_value
            open_total_qty += open_blnc_qty
            close_total_qty += close_blnc_qty
            inward_total_qty += inward_qty
            outward_total_qty += outward_qty

        # print(open_total_value)
        # print(close_total_value)
        # print(inward_total_value)
        # print(outward_total_value)
        # print(open_total_qty)
        # print(close_total_qty)
        # print(inward_total_qty)
        # print(outward_total_qty)
        profit_loss_total = (close_total_value + outward_total_value) - (open_total_value + inward_total_value)
        # print("Profit Loss", profit_loss_total)
        data = {
            'products': prev_month_closing,
            'start_date': start_date,
            'end_date': end_date,
            'open_total_value': round(open_total_value, 3),
            'close_total_value': round(close_total_value, 3),
            'inward_total_value': round(inward_total_value, 3),
            'outward_total_value': round(outward_total_value, 3),
            'open_total_qty': round(open_total_qty, 3),
            'close_total_qty': round(close_total_qty, 3),
            'inward_total_qty': round(inward_total_qty, 3),
            'outward_total_qty': round(outward_total_qty, 3),
            'total_damage': round(total_damage, 3),
            'profit_loss_total': round(profit_loss_total, 2),
        }
        return (self.env.ref('tuba_llc.report_tuba_inventory').with_context(landscape=True)
                .report_action(self, data=data))
