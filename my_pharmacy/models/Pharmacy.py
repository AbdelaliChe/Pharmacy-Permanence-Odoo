from odoo import api, models, fields

class Pharmacy(models.Model):
    _name = 'pharmacy.pharmacy'
    _description = 'Pharmacy Pharmacy'
    _rec_name = 'short_name'

    short_name = fields.Char('Short Title', required=True)
    name = fields.Char('Title', required=True)
    neighborhood = fields.Many2one('pharmacy.neighborhood', string='Neighborhood', help='Select Neighborhood', required=True)
    country = fields.Many2one('res.country', string='Country', default=lambda self: self.env.ref('base.ma', raise_if_not_found=False), readonly=True)
    city = fields.Many2one('pharmacy.city', string='City', help='Select City', required=True)
    phone = fields.Char('Phone', required=True)
    dateStartPermanence = fields.Datetime('Start of Permanence')
    dateEndPermanence = fields.Datetime('End of Permanence')
    permanenceState = fields.Selection(
        [('noPermanence', 'NoPermanence'),
        ('permanence', 'Permanence')],
        'State', default="noPermanence")
    description = fields.Html('Description')
    logo = fields.Binary('Pharmacy Logo')
    medicines = fields.Many2many('pharmacy.medicine', string='Medicines', help='Select Medicines')

    @api.onchange('city')
    def _onchange_city(self):
        if self.city:
            return {'domain': {'neighborhood': [('city_id', '=', self.city.id)]}}
        else:
            return {'domain': {'neighborhood': []}}


    def make_permanent(self):
        self.ensure_one()
        self.permanenceState = 'permanence'

    def make_non_permanent(self):
        self.ensure_one()
        self.permanenceState = 'noPermanence'
