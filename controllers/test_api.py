"""-c /home/med/PycharmProjects/odoo17/odoo17.conf -u app_one -d App_one"""

from odoo import http


class TestApi(http.Controller):

    @http.route('/api/test', methods=["GET"], type="http", auth="none", csrf=False)
    def test_endpoint(self):
        print("inside test_endpoint method")
