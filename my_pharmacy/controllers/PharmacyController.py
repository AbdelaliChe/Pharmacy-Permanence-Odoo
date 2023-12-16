from odoo import http
from odoo.http import request

class PharmacyController(http.Controller):
    @http.route('/pharmacy', auth="public", website=True)
    def pharmacy_page(self, search="", search_in="Name"):
        search_list = {
            'Name': {'label': 'Pharmacy Name', 'input': 'name', 'domain': [('name', 'ilike', search)]},
            'City': {'label': 'City', 'input': 'city', 'domain': [('city', 'ilike', search)]}
        }
        
        search_domain = search_list.get(search_in, {}).get('domain', [])

        pharmacies = request.env['pharmacy.pharmacy'].search(search_domain)
        return http.request.render('my_pharmacy.pharmacy', {'pharmacies': pharmacies, 'search': search, 'search_in': search_in})