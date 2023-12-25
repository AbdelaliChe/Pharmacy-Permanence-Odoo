from odoo import models, fields
from datetime import datetime,timedelta
from difflib import SequenceMatcher
import logging

_logger = logging.getLogger(__name__)

class Permanence(models.Model):
    _name = 'pharmacy.permanence'
    _description = 'Pharmacy Permanence'
    _rec_name = 'short_name'

    short_name = fields.Char('Short name')
    name = fields.Char('Name', required=True)
    city = fields.Char('City', required=True)
    garde_status = fields.Char('Garde Status', required=True)

    #setting this method in action automatized in odoo(every day)
    #permanence_model = env['pharmacy.permanence']
    #permanences = permanence_model.sudo().search([])
    #permanences.make_permanent_pharmacies()
    def make_permanent_pharmacies(self):
        pharmacies = self.env['pharmacy.pharmacy'].search([])
        permanences = self.search([('garde_status', '!=', 'Ouvert en ce moment')])

        for pharmacy in pharmacies:
            for perma in permanences:
                name_similarity = self.calculate_similarity(pharmacy.name.lower(), perma.name.lower())
                city_similarity = self.calculate_similarity(pharmacy.city.lower(), perma.city.lower())
                similarity_threshold = 0.8

                if name_similarity >= similarity_threshold and city_similarity >= similarity_threshold:
                    pharmacy.make_permanent()
                    self.update_pharmacy_permanence_dates(pharmacy, perma.garde_status)
                    #break
                else:
                    pharmacy.make_non_permanent()


    def update_pharmacy_permanence_dates(self, pharmacy, garde_status):
        _logger.info(f"Updating dates for pharmacy: {pharmacy.name}, Garde Status: {garde_status}")
        now = fields.Datetime.now()
        if "24" in garde_status:
            _logger.info("Debug: '24' found in garde_status")
            pharmacy.dateStartPermanence = datetime(now.year, now.month, now.day, 0, 0, 0)
            pharmacy.dateEndPermanence = pharmacy.dateStartPermanence + timedelta(days=1)
        elif "9" in garde_status:
            _logger.info("Debug: '9h' and '23h' found in garde_status")
            pharmacy.dateStartPermanence = datetime(now.year, now.month, now.day, 9, 0, 0)
            pharmacy.dateEndPermanence = datetime(now.year, now.month, now.day, 23, 0, 0)

    #similarity
    def calculate_similarity(self, str1, str2):
        matcher = SequenceMatcher(None, str1, str2)
        return matcher.ratio()
