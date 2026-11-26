import pytest

from carrito.pricing import costo_envio, descuento_cantidad


def test_envio_se_cobra_si_el_descuento_por_cantidad_deja_el_subtotal_bajo_50():
    c = {
        "items": [
            {"precio": 10.133333333333333, "cantidad": 3},
            {"precio": 20.10, "cantidad": 1},
        ],
        "cupon": None,
    }

    assert descuento_cantidad(c) == 1.52
    assert costo_envio(c) == 4.99
