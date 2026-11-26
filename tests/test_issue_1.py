import pytest

from carrito.models import Carrito, item
from carrito.pricing import descuento_cantidad


def test_descuento_cantidad_del_cargador():
    c = Carrito(items=[item("cargador", 1)], cupon="VERANO20", envio=4.99)

    assert descuento_cantidad(c) == 1.52