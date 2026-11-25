from carrito.models import Carrito, item
from carrito.pricing import descuento_cantidad


def test_descuento_cantidad_para_tres_unidades():
    c = Carrito(items=[item("funda", 3)])

    assert descuento_cantidad(c) == 1.52
