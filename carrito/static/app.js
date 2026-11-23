const estado = {
  items: [],
  cupon: null,
  catalogo: [],
  quote: null,
};

const $ = (id) => document.getElementById(id);

const fmt2 = (n) =>
  new Intl.NumberFormat("es-ES", { style: "currency", currency: "EUR" }).format(n);

function badgeCount() {
  return estado.items.reduce((s, i) => s + i.cantidad, 0);
}

function renderCatalogo() {
  const root = $("catalogo");
  root.innerHTML = estado.catalogo
    .map(
      (p) => `
      <article class="card">
        <img src="${p.imagen}" alt="${p.nombre}">
        <div class="card-body">
          <h3>${p.nombre}</h3>
          <p class="precio">${fmt2(p.precio)}</p>
          <button type="button" data-sku="${p.sku}">Añadir a la bolsa</button>
        </div>
      </article>`
    )
    .join("");
  root.querySelectorAll("button[data-sku]").forEach((btn) => {
    btn.addEventListener("click", () => add(btn.dataset.sku));
  });
}

function producto(sku) {
  return estado.catalogo.find((p) => p.sku === sku);
}

function renderBolsa() {
  $("badge").textContent = String(badgeCount());
  const vacio = estado.items.length === 0;
  $("vacio").hidden = !vacio;
  $("lineas").innerHTML = estado.items
    .map((i) => {
      const p = producto(i.sku);
      return `
        <li>
          <img src="${p.imagen}" alt="">
          <div>
            <h4>${p.nombre}</h4>
            <div class="qty">
              <button type="button" data-act="dec" data-sku="${i.sku}" aria-label="Quitar uno">−</button>
              <span>${i.cantidad}</span>
              <button type="button" data-act="inc" data-sku="${i.sku}" aria-label="Añadir uno">+</button>
            </div>
          </div>
          <div class="importe">${fmt2(p.precio * i.cantidad)}</div>
        </li>`;
    })
    .join("");
  $("lineas").querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (btn.dataset.act === "inc") add(btn.dataset.sku);
      else dec(btn.dataset.sku);
    });
  });
  renderResumen();
}

function renderResumen() {
  const q = estado.quote;
  const box = $("resumen");
  if (!q) {
    box.innerHTML = "";
    return;
  }
  const lineas = [
    ["Subtotal", fmt2(q.subtotal)],
    ["Cupón" + (q.cupon ? ` (${q.cupon})` : ""), q.descuento_cupon ? `− ${fmt2(q.descuento_cupon)}` : fmt2(0)],
    ["Dto. cantidad (5 %)", q.descuento_cantidad ? `− ${fmt2(q.descuento_cantidad)}` : fmt2(0)],
    ["Envío", fmt2(q.envio)],
    ["IVA 21 %", fmt2(q.iva_importe)],
  ];
  box.innerHTML =
    lineas.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("") +
    `<div class="total"><span>Total</span><span class="total-valor">${q.total_repr}</span></div>`;
}

async function cotizar() {
  const res = await fetch("/api/cotizar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items: estado.items, cupon: estado.cupon }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "error al cotizar");
  estado.quote = data;
  renderBolsa();
}

function add(sku) {
  const found = estado.items.find((i) => i.sku === sku);
  if (found) found.cantidad += 1;
  else estado.items.push({ sku, cantidad: 1 });
  cotizar();
}

function dec(sku) {
  const found = estado.items.find((i) => i.sku === sku);
  if (!found) return;
  found.cantidad -= 1;
  if (found.cantidad < 1) estado.items = estado.items.filter((i) => i.sku !== sku);
  cotizar();
}

$("vaciar").addEventListener("click", () => {
  estado.items = [];
  cotizar();
});

$("form-cupon").addEventListener("submit", (ev) => {
  ev.preventDefault();
  const code = $("cupon").value.trim().toUpperCase();
  estado.cupon = code || null;
  cotizar().then(() => {
    let aviso = $("form-cupon").querySelector(".aviso");
    if (!aviso) {
      aviso = document.createElement("p");
      aviso.className = "aviso";
      $("form-cupon").appendChild(aviso);
    }
    if (!estado.cupon) {
      aviso.textContent = "Cupón quitado.";
      aviso.className = "aviso";
    } else if (estado.quote.cupon_valido) {
      aviso.textContent = "Cupón aplicado.";
      aviso.className = "aviso ok";
    } else {
      aviso.textContent = "Ese código no existe; no se descuenta nada.";
      aviso.className = "aviso bad";
    }
  });
});

$("abrir-bolsa").addEventListener("click", () => {
  $("bolsa").classList.toggle("abierta");
});

async function boot() {
  const res = await fetch("/api/catalogo");
  const data = await res.json();
  estado.catalogo = data.productos;
  $("cupones-hint").innerHTML =
    "Prueba " + data.cupones.map((c) => `<code>${c}</code>`).join(" · ");
  renderCatalogo();
  await cotizar();
}

boot().catch((err) => {
  $("catalogo").innerHTML = `<p class="vacio">${err.message}</p>`;
});
