from django.test import TestCase
from price_m2.models import Alcaldia, CatastroInfo, UsoConstruccion


def generate_price_m2_data(test_case: TestCase):
    """Registra dos elementos `CatastroInfo` para testear price_m2.
    Adicinalmente registra una `Alcaldia` y un `UsoConstruccion`.

    Ejemplo de uso:

        class My_TestCase(TestCase):

            def setUp(self):
                ...
                generate_price_m2_data(self)
                ...

    Los valores esperados son:

    * avg
        price_unit = 67.11764705882354
        price_unit_construction = 29.470588235294116
    * max
        price_unit = 77
        price_unit_construction = 37
    * min
        price_unit = 57.23529411764706,
        price_unit_construction = 21.941176470588232,
    """

    test_case.alcaldia = Alcaldia.objects.create(name="Álvaro Obregón")
    test_case.uso_construccion = UsoConstruccion.objects.create(
        id=1, name="Habitacional"
    )

    test_case.test_data = (
        # price_unit = (1000 / 10) - 23 = 77
        # price_unit_construction = (600 / 10) - 23 = 37
        CatastroInfo(
            alcaldia=test_case.alcaldia,
            uso_construccion=test_case.uso_construccion,
            codigo_postal="10101",
            superficie_terreno=1000,
            superficie_construccion=600,
            valor_suelo=10,
            subsidio=23,
        ),
        # price_unit = (1500 / 17) - 31 = 57.2352941176
        # price_unit_construction = (900 / 17) - 31 = 21.9411764706
        CatastroInfo(
            alcaldia=test_case.alcaldia,
            uso_construccion=test_case.uso_construccion,
            codigo_postal="10101",
            superficie_terreno=1500,
            superficie_construccion=900,
            valor_suelo=17,
            subsidio=31,
        ),
    )

    CatastroInfo.objects.bulk_create(test_case.test_data)
