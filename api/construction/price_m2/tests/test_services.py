import unittest.mock
from typing import override

from django.test import TestCase
from price_m2.services import (
    PriceM2ServiceBase,
    PriceM2ServiceFactory,
    ServiceError,
)

from .data_price_m2 import generate_price_m2_data


class PriceM2Service_TestCaseBase(TestCase):

    def setUp(self):
        generate_price_m2_data(self)


class AvgPriceM2Service_Agreggation_TestCase(PriceM2Service_TestCaseBase):

    def setUp(self):
        super().setUp()
        self.price_m2_service = PriceM2ServiceFactory.MakeByAggregate("avg")

    def test_calculate(self):
        expected_price_unit = 67.11764705882354
        expected_price_unit_construction = 29.470588235294116

        result = self.price_m2_service.calculate(
            zip_code="10101",
            construction_type=1,
        )

        self.assertEqual(result["type"], "avg")
        self.assertEqual(result["elements"], 2)
        self.assertAlmostEqual(result["price_unit"], expected_price_unit)
        self.assertAlmostEqual(
            result["price_unit_construction"], expected_price_unit_construction
        )


class MaxPriceM2Service_Agreggation_TestCase(PriceM2Service_TestCaseBase):

    def setUp(self):
        super().setUp()
        self.price_m2_service = PriceM2ServiceFactory.MakeByAggregate("max")

    def test_calculate(self):
        expected_price_unit = 77
        expected_price_unit_construction = 37

        result = self.price_m2_service.calculate(
            zip_code="10101",
            construction_type=1,
        )

        self.assertEqual(result["type"], "max")
        self.assertEqual(result["elements"], 2)
        self.assertAlmostEqual(result["price_unit"], expected_price_unit)
        self.assertAlmostEqual(
            result["price_unit_construction"], expected_price_unit_construction
        )


class MinPriceM2Service_Agreggation_TestCase(PriceM2Service_TestCaseBase):

    def setUp(self):
        super().setUp()
        self.price_m2_service = PriceM2ServiceFactory.MakeByAggregate("min")

    def test_calculate(self):
        expected_price_unit = 57.23529411764706
        expected_price_unit_construction = 21.941176470588232

        result = self.price_m2_service.calculate(
            zip_code="10101",
            construction_type=1,
        )

        self.assertEqual(result["type"], "min")
        self.assertEqual(result["elements"], 2)
        self.assertAlmostEqual(result["price_unit"], expected_price_unit)
        self.assertAlmostEqual(
            result["price_unit_construction"], expected_price_unit_construction
        )


class PriceM2Service_InvalidFields_TestCase(PriceM2Service_TestCaseBase):

    class TestPriceM2Service(PriceM2ServiceBase):

        @override
        def calculate(self, zip_code: str, construction_type: int):
            aggregate_mock = unittest.mock.MagicMock()
            aggregate_mock.name = "test-aggregate"

            return self._calculate(zip_code, aggregate_mock, construction_type)

    def setUp(self):
        super().setUp()
        self.price_m2_service = self.TestPriceM2Service()

    @unittest.mock.patch("logging.warning")
    def test_invalid_zip_code(self, warning_mock):
        with self.assertRaises(ServiceError) as ctx_error:
            # El código postal "99999" no está registrado en db por `tests.data_price_m2`
            self.price_m2_service.calculate(
                zip_code="99999", construction_type=1
            )

        self.assertEqual(
            str(ctx_error.exception), "No se halló el código zip solicitado"
        )
        warning_mock.assert_called_once_with(
            "Error buscando zip_code=%s. Info: aggregate=%s, construction_type=%s",
            "99999",
            "test-aggregate",
            1,
        )

    @unittest.mock.patch("logging.warning")
    def test_no_construction_type(self, warning_mock):
        with self.assertRaises(ServiceError) as ctx_error:
            # El tipo de construcción 99 no está registrado en db por `tests.data_price_m2`
            self.price_m2_service.calculate(
                zip_code="10101", construction_type=99
            )

        self.assertEqual(
            str(ctx_error.exception), "No se halló el tipo de construcción"
        )
        warning_mock.assert_called_once_with(
            "Error buscando construction_type=%s. Info: zip_code=%s, aggregate=%s",
            99,
            "10101",
            "test-aggregate",
        )
