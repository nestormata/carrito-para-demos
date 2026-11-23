"""La tienda demo habla con el motor de precios; no cubre los bordes de pricing."""

import pytest

from carrito.web import catalogo_publico, cotizar


def test_catalogo_tiene_seis_productos_con_imagen():
    data = catalogo_publico()
    assert len(data["productos"]) == 6
    skus = {p["sku"] for p in data["productos"]}
    assert skus == {"cable", "funda", "adaptador", "soporte", "cargador", "auriculares"}
    for p in data["productos"]:
        assert p["imagen"].startswith("/static/img/")
        assert p["imagen"].endswith(".jpg")


def test_cotizar_carrito_vacio_incluye_envio():
    q = cotizar({"items": []})
    assert q["unidades"] == 0
    assert q["envio"] == 4.99
    assert q["total"] == pytest.approx(6.04, abs=0.01)


def test_cotizar_sku_desconocido():
    with pytest.raises(ValueError, match="sku desconocido"):
        cotizar({"items": [{"sku": "nope", "cantidad": 1}]})
