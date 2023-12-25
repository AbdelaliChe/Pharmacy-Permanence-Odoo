from odoo import http
from odoo.http import request
from math import radians, sin, cos, sqrt, atan2

class PharmacyController(http.Controller):

    @http.route('/pharmacy', auth="public", website=True)
    def pharmacy_page(self, search="", city_filter="", permanence_filter="", latitude=None, longitude=None, show_more=False):
        
        search_domain = []

        all_cities = request.env['pharmacy.pharmacy'].sudo().search([('city', '!=', False)]).mapped('city')
        cities = set(all_cities)

        if search:
            search_domain += [('name', 'ilike', '%' + search + '%')]
            show_more = True

        if city_filter:
            search_domain += [('city', '=', city_filter)]
            show_more = True

        if permanence_filter:
            search_domain += [('permanenceState', '=', permanence_filter)]
            show_more = True

        pharmacies = request.env['pharmacy.pharmacy'].search(search_domain)

        if latitude and longitude:
            search_domain += [('latitude', '=', float(latitude)), ('longitude', '=', float(longitude))]
            user_location = (float(latitude), float(longitude))
            # Create a list of tuples containing pharmacy records and distances
            pharmacies_with_distances = [(pharmacy, self.haversine(user_location, (pharmacy.latitude, pharmacy.longitude))) for pharmacy in pharmacies]
            # Sort pharmacies by distance
            sorted_pharmacies = sorted(pharmacies_with_distances, key=lambda x: x[1])
            # Extract sorted pharmacy records from the list
            sorted_pharmacies = [record[0] for record in sorted_pharmacies]
            pharmacies = sorted_pharmacies
            show_more = True

        if not show_more:
            pharmacies = pharmacies[:12]

        return http.request.render('my_pharmacy.pharmacy', {
            'pharmacies': pharmacies,
            'search': search,
            'cities': cities,
            'city_filter': city_filter,
            'permanence_filter' : permanence_filter,
            'show_more': show_more,
            'latitude': latitude,
            'longitude': longitude, 
        })
    
    @http.route('/pharmacy/detail/<int:pharmacy_id>', auth="public", website=True)
    def pharmacy_detail_page(self, pharmacy_id , search_name="", show_more=False):
        pharmacy_id = int(pharmacy_id)
       
        pharmacy_stock = request.env['pharmacy.stock'].sudo().search([('pharmacie_id.id', '=', pharmacy_id)])


        medicines = []
        
        for st in pharmacy_stock:
            medic = st.medicament_id
            medicines.append(medic)

        search_domain = [('name', 'ilike', '%' + search_name + '%')]

       
        
        if not show_more:
            medicines = medicines[:12]

        if search_name:
            show_more = True
            medicines = medicines.search(search_domain)

        return http.request.render('my_pharmacy.pharmacy_detail', {
            'pharmacy': pharmacy_stock.pharmacie_id,
            'medicines': medicines,
            'search_name': search_name,
            'show_more': show_more,
        })


    def haversine(self, coord1, coord2):
        # Calculate the distance between two coordinates using the Haversine formula
        # Coordinates are given as (latitude, longitude)
        R = 6371.0  # Earth radius in kilometers

        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c  # Distance in kilometers
        return distance * 1000.0  # Convert to meters