from django.test import Client, TestCase

from .data_price_m2 import generate_price_m2_data


class PriceM2_Integration_TestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        generate_price_m2_data(self)

    def test_price_m2_calculate_avg(self):
        response = self.client.get(
            "/price-m2/zip-codes/10101/aggregate/avg?construction_type=1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "status": True,
                "payload": {
                    "type": "avg",
                    "price_unit": 67.11764705882354,
                    "price_unit_construction": 29.470588235294116,
                    "elements": 2,
                },
            },
        )

    def test_price_m2_calculate_max(self):
        response = self.client.get(
            "/price-m2/zip-codes/10101/aggregate/max?construction_type=1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "status": True,
                "payload": {
                    "type": "max",
                    "price_unit": 77,
                    "price_unit_construction": 37,
                    "elements": 2,
                },
            },
        )

    def test_price_m2_calculate_min(self):
        response = self.client.get(
            "/price-m2/zip-codes/10101/aggregate/min?construction_type=1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "status": True,
                "payload": {
                    "type": "min",
                    "price_unit": 57.23529411764706,
                    "price_unit_construction": 21.941176470588232,
                    "elements": 2,
                },
            },
        )

    def test_invalid_zip_code(self):
        response = self.client.get(
            "/price-m2/zip-codes/NOT-VALID/aggregate/max?construction_type=1"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "status": False,
                "errors": ["No se halló el código zip solicitado"],
            },
        )

    def test_invalid_construction_type(self):
        response = self.client.get(
            "/price-m2/zip-codes/10101/aggregate/avg?construction_type=NOT_VALID"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "status": False,
                "errors": [
                    "Query-parameter `construction_type` inválido: Uso: '?construction_type={1-7}'"
                ],
            },
        )
