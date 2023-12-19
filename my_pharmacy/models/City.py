from odoo import models, fields

class City(models.Model):
    _name = 'pharmacy.city'
    _description = 'Pharmacy City'

    name = fields.Char(string='Name', required=True)
    country_id = fields.Many2one('res.country', string='Country', default=lambda self: self.env.ref('base.ma', raise_if_not_found=False), readonly=True)
