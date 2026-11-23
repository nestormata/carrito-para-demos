# carrito

Motor de precios y tienda de demostración para una tienda pequeña: catálogo
de 6 accesorios, cupones, descuento por cantidad, envío fijo e IVA.

Proyecto creado para el laboratorio de sistemas multi-agente de AI4Devs.
Sirve para ver el motor de precios en una página, abrir issues y
proponer arreglos. Úsalo, fórkalo y rompe cosas: los issues están ahí para eso.

## Para qué es la aplicación

`python3 -m carrito` levanta una **tienda web local**. No es un ecommerce
de producción: no hay cuentas, pagos ni base de datos. Es una vitrina
para el laboratorio:

- Recorrer el catálogo con fotos de ejemplo.
- Meter productos en la bolsa, cambiar cantidades y vaciarla.
- Aplicar un cupón y ver subtotal, descuentos, envío, IVA y total.
- Comprobar que esos números salen del mismo motor Python que usan los tests
  (`carrito.pricing`), no de JavaScript.

La página muestra el total tal como lo devuelve Python (incluido el
`repr` del float), para que coincida con lo que imprime la librería.

## Cómo correrla

Requisitos: Python ≥ 3.10. Cero dependencias de ejecución (solo stdlib).

Desde la **raíz de este repositorio**:

```bash
cd /ruta/a/carrito
python3 -m carrito
```

Eso arranca un servidor HTTP en [http://127.0.0.1:8765](http://127.0.0.1:8765).
Abre esa URL en el navegador. Para parar el servidor: `Ctrl+C` en la terminal.

Host y puerto opcionales:

```bash
python3 -m carrito --host 127.0.0.1 --port 8765
```

`--host 0.0.0.0` deja entrar desde otras máquinas de la red local
(útil si proyectas la demo en otra pantalla).

### En la página

1. Pulsa **Añadir a la bolsa** en un accesorio (cable, funda, adaptador,
   soporte, cargador, auriculares).
2. Ajusta cantidades con `+` / `−` o **Vaciar**.
3. Escribe un cupón y pulsa **Aplicar**. Códigos válidos:
   `BIENVENIDA10`, `VERANO20`, `BLACKFRIDAY30`.
4. El resumen (subtotal, cupón, 5 % por cantidad, envío 4,99 €, IVA 21 %,
   total) se recalcula en el servidor en cada cambio.

Política de la tienda (también al pie de la página): precios en EUR;
los cupones aplican solo sobre productos, nunca sobre el envío; 5 % de
descuento al alcanzar 3 o más unidades; IVA al final.

## Uso como librería

```python
from carrito.models import Carrito, item
from carrito.pricing import total

c = Carrito(items=[item("cable", 2)], cupon="BIENVENIDA10")
print(total(c))
```

## Alcance

- Precios en **EUR**.
- Cálculo local: catálogo fijo, cupones fijos, envío fijo, IVA fijo.
- Sin red, sin APIs externas, sin tipos de cambio, sin persistencia.
- Sin dependencias de ejecución (Python ≥ 3.10).
- La tienda web es solo local (stdlib `http.server`); no hay autenticación
  ni carrito persistente.

Lo que pida servicio externo, otra moneda o una decisión de producto
nueva queda fuera de este repositorio.

## Desarrollo

```bash
python -m pytest -q
```

## Licencia

MIT
