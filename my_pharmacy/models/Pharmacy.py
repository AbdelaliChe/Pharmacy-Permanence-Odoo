from odoo import api, models, fields
import requests, base64

class Pharmacy(models.Model):
    _name = 'pharmacy.pharmacy'
    _description = 'Pharmacy Pharmacy'
    _rec_name = 'short_name'

    short_name = fields.Char('Short Name', required=True)
    name = fields.Char('Name', required=True)
    country = fields.Many2one('res.country', string='Country', default=lambda self: self.env.ref('base.ma', raise_if_not_found=False), readonly=True)
    city = fields.Char('City', required=True)
    address = fields.Char('address')
    dateStartPermanence = fields.Datetime('Start of Permanence')
    dateEndPermanence = fields.Datetime('End of Permanence')
    localisation_link = fields.Char("Link to pharamcy localisation")

    permanenceState = fields.Selection(
        [('Permanence', 'Permanence'),
        ('NonPermanence', 'NonPermanence')],
        'State', default="NonPermanence")
    logo = fields.Binary('Pharmacy Logo')
    medicines = fields.Many2many('pharmacy.medicine', string='Medicines', help='Select Medicines')
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')


    def make_permanent(self):
        self.ensure_one()
        self.permanenceState = 'Permanence'

    def make_non_permanent(self):
        self.ensure_one()
        self.permanenceState = 'NonPermanence'

    #get cities fro data/Morocco_cities.txt
    cities = []
    
    #for fetching all pharamcies from morocco using google map api
    #through the action automized
    #allready done so for saving time just upload the file in data->pharamcy.pharmacy
    @api.model
    def fetch_and_populate_all_pharmacies(self):
        api_key = 'AIzaSyAkyKJTs4TBvQ-2-lmpjmFaNop8Kz-luhg'
        for city_name in self.cities:
            self.fetch_and_populate_pharmacies(api_key, city_name)

    def fetch_and_populate_pharmacies(self, api_key, city_name, page_token=None):
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        query = f"pharmacies in {city_name} Morocco"
        params = {'query': query, 'key': api_key}

        if page_token:
            params['pagetoken'] = page_token

        response = requests.get(base_url, params=params)
        data = response.json()

        pharmacies = data.get('results', [])
        for pharmacy_data in pharmacies:
            self.create_or_update_from_google_places(pharmacy_data, city_name)

        next_page_token = data.get('next_page_token')

        if next_page_token:
            self.fetch_and_populate_pharmacies(api_key, city_name, page_token=next_page_token)

    def create_or_update_from_google_places(self, pharmacy_data, city_name):
        pharmacy_name = pharmacy_data.get('name')
        existing_pharmacy = self.search([('name', '=', pharmacy_name)], limit=1)

        pharmacy_values = {
            'short_name': pharmacy_name,
            'name': pharmacy_name,
            'city': city_name,
            'address': pharmacy_data.get('formatted_address', ''),
            'latitude': pharmacy_data['geometry']['location'].get('lat') if 'geometry' in pharmacy_data and 'location' in pharmacy_data['geometry'] else 0.0,
            'longitude': pharmacy_data['geometry']['location'].get('lng') if 'geometry' in pharmacy_data and 'location' in pharmacy_data['geometry'] else 0.0,
            'logo': self._fetch_and_encode_image(pharmacy_data.get('photos', [])),
            'localisation_link': 'https://www.google.com/maps/search/?api=1&query=' + pharmacy_name + '+in+' + city_name
        }

        if existing_pharmacy:
            existing_pharmacy.write(pharmacy_values)
        else:
            self.create(pharmacy_values)

    def _fetch_and_encode_image(self, photos):
        try:
            if photos:
                photo_reference = photos[0].get('photo_reference', '')
                if photo_reference:
                    api_key = 'AIzaSyAkyKJTs4TBvQ-2-lmpjmFaNop8Kz-luhg'
                    image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=200&photoreference={photo_reference}&key={api_key}"
                    response = requests.get(image_url)

                    if response.status_code == 200:
                        image_data = base64.b64encode(response.content)
                        return image_data
        except Exception as e:
            # Handle errors or log them as needed
            pass

        return b''
