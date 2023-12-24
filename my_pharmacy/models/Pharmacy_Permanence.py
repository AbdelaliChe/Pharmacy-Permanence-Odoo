from odoo import models, fields
from datetime import datetime,timedelta

class Permanence(models.Model):
    _name = 'pharmacy.permanence'
    _description = 'Pharmacy Permanence'
    _rec_name = 'short_name'

    short_name = fields.Char('Short name')
    name = fields.Char('Name', required=True)
    city = fields.Char('City', required=True)
    garde_status = fields.Char('Garde Status', required=True)

    def make_permanent_pharmacies(self):
        for perma in self:
            pharmacies = self.env['pharmacy.pharmacy'].search([])
            for pharmacy in pharmacies:
                name_distance = self.calculate_edit_distance(pharmacy.name.lower(), perma.name.lower())

                threshold = 3

                if name_distance <= threshold:
                    pharmacy.make_permanent()
                    self.update_pharmacy_permanence_dates(pharmacy, perma.garde_status)
                else:
                    pharmacy.make_non_permanent()

    def update_pharmacy_permanence_dates(self, pharmacy, garde_status):
        now = fields.Datetime.now()
        if garde_status == "Ouvert toute la journée (24 heures)":
            pharmacy.dateStartPermanence = datetime(now.year, now.month, now.day, 0, 0, 0)
            pharmacy.dateEndPermanence = pharmacy.dateStartPermanence + timedelta(days=1)
        elif garde_status == "Garde Jour (Ouvert entre 9h et 23h)":
            pharmacy.dateStartPermanence = datetime(now.year, now.month, now.day, 9, 0, 0)
            pharmacy.dateEndPermanence = pharmacy.dateStartPermanence.replace(hour=23, minute=0, second=0, microsecond=0)


    #string distance 
    #string distance 
    def calculate_edit_distance(self, str1, str2):
        m = len(str1)
        n = len(str2)

        # Create a matrix to store the edit distances
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize the first row and column of the matrix
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Fill in the matrix using dynamic programming
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # If the characters are the same, no operation needed
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Calculate the cost of deletion, insertion, and substitution
                    deletion_cost = dp[i - 1][j] + 1
                    insertion_cost = dp[i][j - 1] + 1
                    substitution_cost = dp[i - 1][j - 1] + 1

                    # Choose the minimum cost among the three options
                    dp[i][j] = min(deletion_cost, min(insertion_cost, substitution_cost))

        # The bottom-right cell of the matrix contains the edit distance
        return dp[m][n]
