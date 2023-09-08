from odoo import models, api


class TubaSupplierReport(models.AbstractModel):
    _name = 'tuba.supplier.report'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'data': data,
        }

