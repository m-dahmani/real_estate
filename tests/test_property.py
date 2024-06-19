"""-c /home/med/PycharmProjects/odoo17/odoo17.conf -u app_one --test-enable"""

from odoo.tests.common import TransactionCase
from odoo import fields


class TestProperty(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp()
        # super(TestProperty, self).setUp()

        self.property_01_record = self.env['property'].create(
            {
                'ref': 'PRT00009',
                'name': 'Property 9',
                'description': 'Property 9 descrip',
                'postcode': '9999',
                'date_availability': fields.Date.today(),
                'expected_price': 10000,
                'bedrooms': 5,
            }
        )

    def test_property_01_values(self):
        property_id = self.property_01_record

        self.assertRecordValues(records=property_id, expected_values=[
            {
                'ref': 'PRT00009',
                'name': 'Property 9',
                'description': 'Property 9 descrip',
                'postcode': '9999',
                'date_availability': fields.Date.today(),
                'expected_price': 10000,
                'bedrooms': 5,
            }
        ])
