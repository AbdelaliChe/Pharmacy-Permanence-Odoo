from odoo import models, fields

class Medicine(models.Model):
    _name = 'pharmacy.medicine'
    _description = 'Pharmacy Medicine'

    name = fields.Char(string='Name', required=True)
    indication = fields.Char("Indication")
    description = fields.Text(string='Description')
    distributer = fields.Char(string='Distributer')
    composition = fields.Text(string='Composition')
    public_price = fields.Monetary(string='Public Price', currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.MAD', raise_if_not_found=False))
    pharmacies = fields.Many2many('pharmacy.pharmacy', string='Pharmacies', help='Select Pharmacies')
    logo = fields.Binary('Pharmacy Logo')
    isInStock = fields.Boolean("Is in Stock?", default=True)
