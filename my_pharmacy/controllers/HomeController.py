from odoo import http
from odoo.http import request

class HomeController(http.Controller):
    @http.route('/', auth="public", website=True)
    def pharmacy_page(self):
        return http.request.render('my_pharmacy.home')