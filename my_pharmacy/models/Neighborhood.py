from odoo import models, fields

class Neighborhood(models.Model):
    _name = 'pharmacy.neighborhood'
    _description = 'Pharmacy Neighborhood'

    name = fields.Char(string='Name', required=True)
    city_id = fields.Many2one('pharmacy.city', string='City', required=True)
