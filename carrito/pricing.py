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


def subtotal(carrito: Carrito) -> float:
    """Suma precio × cantidad de todos los ítems del carrito."""
    return sum(i.precio * i.cantidad for i in carrito.items)


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
    return round((subtotal(carrito) + carrito.envio) * pct, 2)


def descuento_cantidad(carrito: Carrito) -> float:
    """5 % de descuento cuando el pedido alcanza 3 o más unidades."""
    if unidades(carrito) >= 3:
        importe = Decimal(str(subtotal(carrito))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ) * Decimal(str(DTO_CANTIDAD))
        return float(importe.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    return 0.0


def total(carrito: Carrito) -> float:
    """Total del pedido (productos − descuentos + envío) con IVA aplicado al final."""
    base = (
        subtotal(carrito)
        - descuento_cupon(carrito)
        - descuento_cantidad(carrito)
        + carrito.envio
    )
    return base * (1 + IVA)
