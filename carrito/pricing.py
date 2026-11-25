"""Motor de precios de Carrito: subtotal, cupones, descuento por cantidad y total."""

from decimal import Decimal, ROUND_HALF_UP

from carrito.models import Carrito

IVA = 0.21
CUPONES: dict[str, float] = {
    "BIENVENIDA10": 0.10,
    "VERANO20": 0.20,
    "BLACKFRIDAY30": 0.30,
}
DTO_CANTIDAD = 0.05  # 5 %

_CENTIMO = Decimal("0.01")


def _subtotal_decimal(carrito: Carrito) -> Decimal:
    return sum(
        (Decimal(str(i.precio)) * i.cantidad for i in carrito.items),
        start=Decimal("0"),
    )


def _redondear_importe(importe: Decimal) -> float:
    return float(importe.quantize(_CENTIMO, rounding=ROUND_HALF_UP))


def subtotal(carrito: Carrito) -> float:
    """Suma precio × cantidad de todos los ítems del carrito."""
    return float(_subtotal_decimal(carrito))


def unidades(carrito: Carrito) -> int:
    """Número total de unidades en el carrito."""
    return sum(i.cantidad for i in carrito.items)


def descuento_cupon(carrito: Carrito) -> float:
    """Importe descontado por el cupón según la política de cupones.

    La política de la tienda: los cupones aplican ÚNICAMENTE sobre productos,
    nunca sobre el envío.
    """
    if carrito.cupon is None:
        return 0.0
    pct = CUPONES.get(carrito.cupon)
    if pct is None:
        return 0.0
    base = _subtotal_decimal(carrito) + Decimal(str(carrito.envio))
    return _redondear_importe(base * Decimal(str(pct)))


def descuento_cantidad(carrito: Carrito) -> float:
    """5 % de descuento cuando el pedido alcanza 3 o más unidades."""
    if unidades(carrito) >= 3:
        return _redondear_importe(
            _subtotal_decimal(carrito) * Decimal(str(DTO_CANTIDAD))
        )
    return 0.0


def total(carrito: Carrito) -> float:
    """Total del pedido (productos − descuentos + envío) con IVA aplicado al final."""
    base = (
        _subtotal_decimal(carrito)
        - Decimal(str(descuento_cupon(carrito)))
        - Decimal(str(descuento_cantidad(carrito)))
        + Decimal(str(carrito.envio))
    )
    return _redondear_importe(base * (Decimal("1") + Decimal(str(IVA))))
