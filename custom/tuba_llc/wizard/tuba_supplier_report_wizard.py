import logging
from odoo import models, fields, _
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class TubaSupplierReport(models.TransientModel):
    _name = 'tuba.supplier.report.wizard'

    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    report_type = fields.Selection([('cash', 'Cash'), ('simple', 'Simple')],
                                   string="Report Type", required=True, default='simple')
    customer_id = fields.Many2one('res.partner', string="Supplier")

    def check_report(self):
        start_date = self.start_date
        end_date = self.end_date
        open_total = 0.0
        close_total = 0.0
        debit_total = 0.0
        credit_total = 0.0
        if start_date > end_date:
            raise AccessError(_("Start Date Must be Less than from End Date!"))
        customer_id = self.customer_id
        customers = self.env['res.partner'].search([])
        prev_month_closing = []
        for cust in customers:
            total_purchase = 0.0
            current_month_total_purchase = 0.0
            total_payment = 0.0
            current_month_total_payment = 0.0
            purchase_order = self.env['tuba.purchase.order'].search([('new_order_date', '<', start_date),
                                                                     ('customer_id', '=', cust.id)])
            if purchase_order:
                for sale in purchase_order:
                    total_purchase += sale.total_amount
            payment = self.env['supplier.payment'].search([('new_payment_date', '<', start_date),
                                                           ('customer_id', '=', cust.id)])
            if payment:
                for pay in payment:
                    total_payment += pay.payment

            current_month_purchase_order = self.env['tuba.purchase.order'].search([('new_order_date', '>=', start_date),
                                                                                   ('new_order_date', '<=', end_date),
                                                                                   ('customer_id', '=', cust.id)])
            if current_month_purchase_order:
                for purchase in current_month_purchase_order:
                    current_month_total_purchase += purchase.total_amount
            current_month_payment = self.env['supplier.payment'].search([('new_payment_date', '>=', start_date),
                                                                         ('new_payment_date', '<=', end_date),
                                                                         ('customer_id', '=', cust.id)])
            if current_month_payment:
                for pay in current_month_payment:
                    current_month_total_payment += pay.payment

            opening_balance = (total_purchase - total_payment) + cust.supplier_opening_balance
            closing_balance = (current_month_total_purchase - current_month_total_payment) + opening_balance
            open_total += opening_balance
            close_total += closing_balance
            credit_total += current_month_total_purchase
            debit_total += current_month_total_payment
            if closing_balance:
                dic = {
                    'name': cust.name,
                    'emirates_id': cust.emirates_id,
                    'mobile': cust.mobile,
                    'credit': total_purchase,
                    'debit': total_payment,
                    'opening_balance': round(opening_balance, 3),
                    'current_credit': round(current_month_total_purchase, 3),
                    'current_debit': round(current_month_total_payment, 3),
                    'closing_balance': round(closing_balance, 3)
                }
                prev_month_closing.append(dic)

        data = {
            'customers': prev_month_closing,
            'start_date': start_date,
            'end_date': end_date,
            'open_total': round(open_total, 2),
            'close_total': round(close_total, 2),
            'debit_total': round(debit_total, 2),
            'credit_total': round(credit_total, 2),
        }
        return self.env.ref('tuba_llc.report_tuba_supplier').report_action(self, data=data)

    # def check_report(self):
    #     start_date = self.start_date
    #     end_date = self.end_date
    #     if start_date >= end_date:
    #         raise AccessError(_("Start Date Must be Less than from End Date!"))
    #     customer_id = self.customer_id
    #     sale_order = self.env['tuba.sale.order'].search([('new_order_date', '<', start_date),
    #                                                      ('customer_id', '=', customer_id.id)])
    #     receiving = self.env['customer.receiving'].search([('new_receiving_date', '<', start_date),
    #                                                        ('customer_id', '=', customer_id.id)])
    #     payment = 0.0
    #     total_amount = 0.0
    #     if sale_order:
    #         for i in sale_order:
    #             total_amount += i.total_amount
    #     if receiving:
    #         for i in receiving:
    #             payment += i.payment
    #
    #     prev_closing_blnc = total_amount - payment
    #     print(prev_closing_blnc)
    #
    #     customers = self.env['res.partner'].search([('id', '=', customer_id.id)])
    #     if customers:
    #         print(customers.name)
    #         print(start_date)
    #         print(end_date)
    #
    #     sale_order = self.env['tuba.sale.order'].search([('new_order_date', '>=', start_date),
    #                                                      ('new_order_date', '<=', end_date),
    #                                                      ('customer_id', '=', customer_id.id)])
    #     receiving = self.env['customer.receiving'].search([('new_receiving_date', '>=', start_date),
    #                                                        ('new_receiving_date', '<=', end_date),
    #                                                        ('customer_id', '=', customer_id.id)])
    #     sale_payment = []
    #     receive_payment = []
    #     for sale in sale_order:
    #         dic = {
    #             'credit': sale.total_amount,
    #             'date': sale.new_order_date,
    #         }
    #         sale_payment.append(dic)
    #     for receive in receiving:
    #         dic = {
    #             'debit': receive.payment,
    #             'date': receive.new_receiving_date,
    #         }
    #         receive_payment.append(dic)
    #
    #     print(sale_payment)
    #     print(receive_payment)
    #     data = {
    #         'cust_name': customers.name,
    #         'start_date': start_date,
    #         'end_date': end_date,
    #     }
    #     return self.env.ref('tuba_llc.report_tuba_customer').report_action(self, data=data)
