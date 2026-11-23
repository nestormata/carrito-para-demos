"""Tienda demo: servidor HTTP (stdlib) que cotiza con el motor de precios real."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from carrito.models import CATALOGO, Carrito, item
from carrito.pricing import (
    CUPONES,
    DTO_CANTIDAD,
    IVA,
    descuento_cantidad,
    descuento_cupon,
    subtotal,
    total,
    unidades,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
MIME = {
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}


def catalogo_publico() -> dict:
    productos = [
        {
            "sku": sku,
            "nombre": it.nombre,
            "precio": it.precio,
            "imagen": f"/static/img/{sku}.jpg",
        }
        for sku, it in CATALOGO.items()
    ]
    return {
        "productos": productos,
        "envio": 4.99,
        "iva": IVA,
        "dto_cantidad": DTO_CANTIDAD,
        "cupones": sorted(CUPONES),
    }


def cotizar(payload: dict) -> dict:
    crudos = payload.get("items") or []
    if not isinstance(crudos, list):
        raise ValueError("items debe ser una lista")

    lineas: list = []
    for fila in crudos:
        sku = str(fila.get("sku", "")).strip()
        if sku not in CATALOGO:
            raise ValueError(f"sku desconocido: {sku}")
        try:
            cantidad = int(fila.get("cantidad", 1))
        except (TypeError, ValueError) as exc:
            raise ValueError("cantidad inválida") from exc
        if cantidad < 1:
            raise ValueError("cantidad debe ser ≥ 1")
        lineas.append(item(sku, cantidad))

    cupon_in = payload.get("cupon")
    cupon = str(cupon_in).strip().upper() if cupon_in else None
    if cupon == "":
        cupon = None

    carrito = Carrito(items=lineas, cupon=cupon)
    sub = subtotal(carrito)
    dto_c = descuento_cupon(carrito)
    dto_q = descuento_cantidad(carrito)
    tot = total(carrito)
    base = sub - dto_c - dto_q + carrito.envio
    return {
        "items": [
            {
                "sku": i.sku,
                "nombre": i.nombre,
                "precio": i.precio,
                "cantidad": i.cantidad,
                "importe": i.precio * i.cantidad,
            }
            for i in lineas
        ],
        "cupon": cupon,
        "cupon_valido": cupon in CUPONES if cupon else False,
        "unidades": unidades(carrito),
        "subtotal": sub,
        "descuento_cupon": dto_c,
        "descuento_cantidad": dto_q,
        "envio": carrito.envio,
        "base": base,
        "iva": IVA,
        "iva_importe": tot - base,
        "total": tot,
        "total_repr": repr(tot),
    }


class TiendaHandler(BaseHTTPRequestHandler):
    server_version = "CarritoDemo/0.1"

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} {fmt % args}")

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, payload: dict) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(code, raw, "application/json; charset=utf-8")

    def do_GET(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path in ("/", "/index.html"):
            self._file(STATIC_DIR / "index.html")
            return
        if path == "/api/catalogo":
            self._json(200, catalogo_publico())
            return
        if path.startswith("/static/"):
            self._file(STATIC_DIR / path[len("/static/") :])
            return
        self._json(404, {"error": "no encontrado"})

    def do_POST(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path != "/api/cotizar":
            self._json(404, {"error": "no encontrado"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
            if not isinstance(payload, dict):
                raise ValueError("cuerpo JSON inválido")
            self._json(200, cotizar(payload))
        except (json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
            self._json(400, {"error": str(exc)})

    def _file(self, candidate: Path) -> None:
        try:
            target = candidate.resolve()
            target.relative_to(STATIC_DIR.resolve())
        except ValueError:
            self._json(403, {"error": "prohibido"})
            return
        if not target.is_file():
            self._json(404, {"error": "no encontrado"})
            return
        data = target.read_bytes()
        ctype = MIME.get(target.suffix.lower(), "application/octet-stream")
        self._send(200, data, ctype)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Tienda demo de Carrito")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    httpd = ThreadingHTTPServer((args.host, args.port), TiendaHandler)
    print(f"Carrito en http://{args.host}:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nadios")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
