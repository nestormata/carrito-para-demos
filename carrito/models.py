"""Modelos de dominio de Carrito: catálogo, ítems y carrito."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Item:
    sku: str
    nombre: str
    precio: float
    cantidad: int = 1


CATALOGO: dict[str, Item] = {
    "cable": Item("cable", "Cable USB-C 1 m", 9.99),
    "funda": Item("funda", "Funda de silicona", 10.10),
    "adaptador": Item("adaptador", "Adaptador HDMI a USB-C", 12.30),
    "soporte": Item("soporte", "Soporte de mesa para portátil", 18.75),
    "cargador": Item("cargador", "Cargador rápido 20 W", 24.50),
    "auriculares": Item("auriculares", "Auriculares bluetooth", 39.90),
}


def item(sku: str, cantidad: int = 1) -> Item:
    """Atajo: crea un Item del catálogo con la cantidad dada."""
    prototipo = CATALOGO[sku]
    return Item(prototipo.sku, prototipo.nombre, prototipo.precio, cantidad)


@dataclass
class Carrito:
    """Carrito de la compra con un cupón opcional y coste de envío fijo."""

    items: list[Item] = field(default_factory=list)
    cupon: str | None = None
    envio: float = 4.99
