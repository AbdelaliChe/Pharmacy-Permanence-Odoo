from odoo import models, fields, api

class Medicine(models.Model):
    _name = 'pharmacy.medicine'
    _description = 'Pharmacy Medicine'

    name = fields.Char(string='Name', required=True)
    forme = fields.Char("Forme")
    presentation = fields.Char(string='Presentation')
    composition = fields.Char(string='Composition')
    price = fields.Monetary(string='Public Price', currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.MAD', raise_if_not_found=False))
    pharmacies = fields.Many2many('pharmacy.pharmacy', string='Pharmacies', help='Select Pharmacies')
    dosage = fields.Char(string='Dosage')
    unit_dosage = fields.Char(string='Unite Dosage')

    @api.model
    def associate_with_all_pharmacies(self):
        pharmacies = self.env['pharmacy.pharmacy'].search([])
        for medicine in self.search([]):
            medicine.write({'pharmacies': [(6, 0, pharmacies.ids)]})