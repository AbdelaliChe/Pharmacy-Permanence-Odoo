from odoo import http
from odoo.http import request

class PharmacyController(http.Controller):

    @http.route('/pharmacy', auth="public", website=True)
    def pharmacy_page(self, search="", search_in="Name", city_filter="", neighborhood_filter="",permanence_filter=""):
        search_list = {
            'Name': {'label': 'Pharmacy Name', 'input': 'name', 'domain': [('name', 'ilike', search)]},
            'City': {'label': 'City', 'input': 'city', 'domain': [('city', 'ilike', search)]}
        }

        search_domain = search_list.get(search_in, {}).get('domain', [])

        all_cities = request.env['pharmacy.city'].search([]).mapped('name')
        cities = set(all_cities)

        all_neighborhoods = request.env['pharmacy.neighborhood'].search([]).mapped('name')
        neighborhoods = set(all_neighborhoods)

        if city_filter:
            search_domain += [('city', '=', city_filter)]
            neighborhoods = request.env['pharmacy.neighborhood'].search([('city_id.name', '=', city_filter)]).mapped('name')

        if neighborhood_filter:
            search_domain += [('neighborhood', '=', neighborhood_filter)]

        if permanence_filter:
            search_domain += [('permanenceState', '=', permanence_filter)]

        pharmacies = request.env['pharmacy.pharmacy'].search(search_domain)

        return http.request.render('my_pharmacy.pharmacy', {
            'pharmacies': pharmacies,
            'search': search,
            'search_in': search_in,
            'cities': cities,
            'neighborhoods' : neighborhoods,
            'city_filter': city_filter,
            'neighborhood_filter' : neighborhood_filter,
            'permanence_filter' : permanence_filter,
        })
    
    @http.route('/pharmacy/detail/<int:pharmacy_id>', auth="public", website=True)
    def pharmacy_detail_page(self, pharmacy_id, search_name=None):
        pharmacy_id = int(pharmacy_id)

        pharmacy = request.env['pharmacy.pharmacy'].sudo().browse(pharmacy_id)

        search_domain = [('name', 'ilike', search_name)] if search_name else []

        medicines = pharmacy.medicines.filtered_domain(search_domain) if search_name else pharmacy.medicines

        return http.request.render('my_pharmacy.pharmacy_detail', {
            'pharmacy': pharmacy,
            'medicines': medicines,
            'search_name': search_name,
        })

