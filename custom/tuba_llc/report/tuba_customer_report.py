from odoo import models, api


class TubaCustomerReport(models.AbstractModel):
    _name = 'tuba.customer.report'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'data': data,
        }

