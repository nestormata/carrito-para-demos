"""Tests del motor de precios."""

import pytest

from carrito.models import Carrito, item
from carrito.pricing import descuento_cantidad, descuento_cupon, subtotal, total, unidades


def test_subtotal_un_articulo():
    c = Carrito(items=[item("cable", 1)])
    assert subtotal(c) == 9.99


def test_subtotal_varios_articulos():
    c = Carrito(items=[item("adaptador", 2), item("cable", 1)])
    assert subtotal(c) == pytest.approx(34.59, abs=1e-6)


def test_unidades():
    c = Carrito(items=[item("funda", 2), item("cable", 1)])
    assert unidades(c) == 3


def test_cupon_aplica_porcentaje():
    c = Carrito(items=[item("cable", 1)], cupon="BIENVENIDA10", envio=0.0)
    assert descuento_cupon(c) == pytest.approx(1.0, abs=0.01)


def test_cupon_invalido_devuelve_cero():
    c = Carrito(items=[item("cable", 1)], cupon="NOEXISTE")
    assert descuento_cupon(c) == 0.0


def test_descuento_cantidad_con_4_unidades():
    c = Carrito(items=[item("cable", 4)])
    assert descuento_cantidad(c) == pytest.approx(2.0, abs=0.01)


def test_total_pedido_basico():
    c = Carrito(items=[item("cable", 2)])
    assert total(c) == pytest.approx(30.21, abs=0.01)


def test_carrito_vacio_solo_envio():
    c = Carrito()
    assert total(c) == pytest.approx(6.04, abs=0.01)
