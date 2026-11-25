import pytest

from carrito.models import Carrito, item
from carrito.pricing import descuento_cantidad


def test_descuento_cantidad_se_aplica_con_exactamente_tres_unidades():
    c = Carrito(items=[item("funda", 3)])

    assert descuento_cantidad(c) == pytest.approx(1.52)
