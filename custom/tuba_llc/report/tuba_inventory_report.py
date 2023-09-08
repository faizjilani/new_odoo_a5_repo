from odoo import models, api


class TubaInventoryReport(models.AbstractModel):
    _name = 'tuba.inventory.report'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'data': data,
        }

