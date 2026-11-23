# carrito

Motor de precios minimalista para una tienda pequeña: catálogo, cupones,
descuento por cantidad, envío e IVA.

Proyecto de demostración creado para el laboratorio de sistemas multi-agente
de AI4Devs. Úsalo, fórkalo y rompe cosas: los issues están ahí para eso.

## Alcance

- Precios en **EUR**.
- Cálculo local: catálogo fijo, cupones fijos, envío fijo, IVA fijo.
- Sin red, sin APIs externas, sin tipos de cambio, sin persistencia.
- Sin dependencias de ejecución (Python ≥ 3.10).

Lo que pida servicio externo, otra moneda o una decisión de producto
nueva queda fuera de este repositorio.

## Uso

```python
from carrito.models import Carrito, item
from carrito.pricing import total

c = Carrito(items=[item("cable", 2)], cupon="BIENVENIDA10")
print(total(c))
```

## Desarrollo

    python -m pytest -q

## Licencia

MIT
