"""Motor de precios de Carrito: subtotal, cupones, descuento por cantidad y total."""

from carrito.models import Carrito

IVA = 0.21
CUPONES: dict[str, float] = {
    "BIENVENIDA10": 0.10,
    "VERANO20": 0.20,
    "BLACKFRIDAY30": 0.30,
}
DTO_CANTIDAD = 0.05  # 5 %
ENVIO_FIJO = 4.99
UMBRAL_ENVIO_GRATIS = 50.00


def _valor(objeto, atributo: str, clave: str):
    if isinstance(objeto, dict):
        return objeto[clave]
    return getattr(objeto, atributo)


def _items(carrito: Carrito):
    return _valor(carrito, "items", "items")


def subtotal(carrito: Carrito) -> float:
    """Suma precio × cantidad de todos los ítems del carrito."""
    return sum(
        _valor(i, "precio", "precio") * _valor(i, "cantidad", "cantidad")
        for i in _items(carrito)
    )


def unidades(carrito: Carrito) -> int:
    """Número total de unidades en el carrito."""
    return sum(_valor(i, "cantidad", "cantidad") for i in _items(carrito))


def descuento_cupon(carrito: Carrito) -> float:
    """Importe descontado por el cupón sobre los productos."""
    cupon = _valor(carrito, "cupon", "cupon")
    if cupon is None:
        return 0.0
    pct = CUPONES.get(cupon)
    if pct is None:
        return 0.0
    return round(subtotal(carrito) * pct, 2)


def descuento_cantidad(carrito: Carrito) -> float:
    """Aplica un 5 % a las líneas que alcanzan 3 unidades."""
    base = sum(
        _valor(i, "precio", "precio") * _valor(i, "cantidad", "cantidad")
        for i in _items(carrito)
        if _valor(i, "cantidad", "cantidad") >= 3
    )
    return round(base * DTO_CANTIDAD, 2)


def costo_envio(carrito: Carrito) -> float:
    """Devuelve el envío fijo, salvo que el subtotal tras descuentos alcance 50 €."""
    base = subtotal(carrito) - descuento_cupon(carrito) - descuento_cantidad(carrito)
    return 0.0 if base >= UMBRAL_ENVIO_GRATIS else ENVIO_FIJO


def total(carrito: Carrito) -> float:
    """Total del pedido (productos − descuentos + envío) con IVA aplicado al final."""
    base = (
        subtotal(carrito)
        - descuento_cupon(carrito)
        - descuento_cantidad(carrito)
        + costo_envio(carrito)
    )
    return base * (1 + IVA)
