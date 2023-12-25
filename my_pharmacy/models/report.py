from odoo import api, models

class ReportMyReport(models.AbstractModel):
    _name = 'report.my_pharmacy_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Get data for the report
        docs = self.env['pharmacy.pharmacy'].browse(docids)
        
        # Return data to be used in the report template
        return {
            'doc_ids': docids,
            'doc_model': 'pharmacy.pharmacy',
            'docs': docs,
        }
    
    @api.model
    def _get_report_name(self):
        return 'my_pharmacy_report.report_my_pharmacy_template'