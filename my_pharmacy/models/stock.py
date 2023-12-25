from odoo import api,models, fields

class Stock(models.Model):
    _name = 'pharmacy.stock'
    _description = 'Pharmacy Stock'

    pharmacie_id = fields.Many2one('pharmacy.pharmacy', string='Pharmacie')
    medicament_id = fields.Many2one('pharmacy.medicine', string='Medicament')
    quantity = fields.Integer(string='Quantity')


    @api.model
    def _auto_init(self):
        res = super(Stock, self)._auto_init()
        self.create_stocks()
        return res

    def create_stocks(self):
        stocks = self.env['pharmacy.stock'].search([], limit=1)
        if len(stocks) == 0:
            
            pharmacies = self.env['pharmacy.pharmacy'].search([])
            medicaments = self.env['pharmacy.medicine'].search([])

            for pharmacy in pharmacies:
                i=0
                for medicament in medicaments:
                    if i==50:
                        break
                    # Check if the stock record already exists
                    existing_stock = self.search([
                        ('pharmacie_id', '=', pharmacy.id),
                        ('medicament_id', '=', medicament.id)
                    ], limit=1)

                    # Create a new stock record if it doesn't exist
                    if not existing_stock:
                        self.create({
                            'pharmacie_id': pharmacy.id,
                            'medicament_id': medicament.id,
                            'quantity': 100  # Set a default quantity or leave it as 0
                        })
                    i = i+1
        return True