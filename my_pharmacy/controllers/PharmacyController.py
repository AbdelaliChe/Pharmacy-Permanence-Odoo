from odoo import http
from odoo.http import request

class PharmacyController(http.Controller):

    @http.route('/pharmacy', auth="public", website=True)
    def pharmacy_page(self, search="", search_in="Name", city_filter="", country_filter="", neighborhood_filter="",permanence_filter=""):
        search_list = {
            'Name': {'label': 'Pharmacy Name', 'input': 'name', 'domain': [('name', 'ilike', search)]},
            'City': {'label': 'City', 'input': 'city', 'domain': [('city', 'ilike', search)]}
        }

        search_domain = search_list.get(search_in, {}).get('domain', [])

        all_cities = request.env['pharmacy.pharmacy'].search([]).mapped('city')
        cities = set(all_cities)

        all_countries = request.env['pharmacy.pharmacy'].search([]).mapped('country')
        countries = set(all_countries)

        all_neighborhoods = request.env['pharmacy.pharmacy'].search([]).mapped('address')
        neighborhoods = set(all_neighborhoods)

        if city_filter:
            search_domain += [('city', '=', city_filter)]

        if country_filter:
            search_domain += [('country', '=', country_filter)]

        if neighborhood_filter:
            search_domain += [('address', '=', neighborhood_filter)]

        if permanence_filter:
            search_domain += [('permanenceState', '=', permanence_filter)]

        pharmacies = request.env['pharmacy.pharmacy'].search(search_domain)

        return http.request.render('my_pharmacy.pharmacy', {
            'pharmacies': pharmacies,
            'search': search,
            'search_in': search_in,
            'cities': cities,
            'countries': countries,
            'neighborhoods' : neighborhoods,
            'city_filter': city_filter,
            'country_filter': country_filter,
            'neighborhood_filter' : neighborhood_filter,
            'permanence_filter' : permanence_filter,
        })
