from odoo import api, models, fields
import requests, base64

class Commande(models.Model):
    _name = 'pharmacy.commande'
    _description = 'Pharmacy Commande'


    code = fields.Integer('Code')
    stock_id = fields.Many2one('pharmacy.stock', string='Stock')
    pharmacie = fields.Many2one(related='stock_id.pharmacie_id', string='Pharmacy', store=True)
    medicament = fields.Many2one(related='stock_id.medicament_id', string='Medicine', store=True)
    commandeBookDate = fields.Datetime('Book Date')
    schedule_cancel_date = fields.Datetime('Scheduled Cancel Date', readonly=True)
    commandeState = fields.Selection(
        [('booked', 'Booked'),
        ('canceled', 'Canceled'),
        ('payed', 'Payed')],
        'State', default="booked")


    def make_booked(self):
        self.ensure_one()
        self.commandeState = 'booked'
    
    def make_canceled(self):
        self.ensure_one()
        self.commandeState = 'canceled'
    
    def make_payed(self):
        self.ensure_one()
        if self.stock_id and self.stock_id.quantity > 0:
            self.stock_id.quantity -= 1
            self.commandeState = 'payed'
        else:
            self.make_canceled()



    def cancel_overdue_commandes(self):
        overdue_commandes = self.search([('commandeState', '=', 'booked'), ('schedule_cancel_date', '<=', fields.Datetime.now())])

        for commande in overdue_commandes:
            commande.make_canceled()
