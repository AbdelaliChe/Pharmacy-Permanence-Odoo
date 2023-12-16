from odoo import api,models,fields
class Pharmacy(models.Model):
    _name = 'pharmacy.pharmacy'
    _description = 'Pharmacy Pharmacy'
    _rec_name = 'short_name'

    short_name = fields.Char('short Title', required=True)
    name = fields.Char('Title',required=True)
    address = fields.Char('Address',required=True)
    country = fields.Many2one('res.country', string='Country', help='Select Country')
    city = fields.Char('City')
    phone = fields.Char('Phone')
    dateStartPermanence = fields.Datetime('Start of Permanence')
    dateEndPermanence = fields.Datetime('End of Permanence')
    isStockEnough = fields.Boolean("is Stock Enough",default=True)
    permanenceState = fields.Selection(
        [('noPermanence','NoPermanence'),
            ('permanence','Permanence')],
        'State',default="noPermanence")
    description = fields.Html('Description')
    logo = fields.Binary('Pharmacy Logo')

    def make_permanent(self):
        self.ensure_one()
        self.permanenceState = 'permanence'

    def make_non_permanent(self):
        self.ensure_one()
        self.permanenceState = 'noPermanence'