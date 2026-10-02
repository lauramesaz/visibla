"""Páginas de venta (por especialidad y por ciudad) y casos de Visibla.

Fuente: _agencia/paginas/<slug>.json → salida /<slug>/index.html (o /casos/<slug>/ si "tipo" = "caso").

Campos del JSON:
  tipo        "especialidad" | "ciudad" | "caso"
  titulo      <title> (≤ 60 car.)          meta     descripción (140–158 car.)
  kicker      texto pequeño sobre el H1      h1       titular: EMPIEZA con la palabra clave ("Agencia SEO para clínicas en X: …"), ≤ 75 car.
  sub         1–2 frases bajo el H1          keyword  palabra clave principal
  wa          mensaje de WhatsApp prellenado
  dolores     [{"t","p"}] ×3  lo que le pasa hoy al lector
  contexto    HTML (h2/h3/p/ul/ol/table/strong/a) específico de la ciudad/especialidad (o la historia del caso)
  incluye     [{"t","p"}] ×4–6  qué hace Visibla para este lector
  guias       [slugs del blog] relacionadas (solo las que existan)
  faq         [{"q","a"}]     fuentes [{"t","u"}]
  fecha, modificado
"""
import json, sys
from datetime import date
from pathlib import Path

PASOS = [
    ("01 — Semana 1", "Revisamos tu clínica", "Tu web, tu ficha de Google, tus reseñas y a tu competencia. Sabemos en qué estás perdiendo pacientes."),
    ("02 — Desde el día 8", "El agente publica", "Un artículo nuevo al día sobre lo que tus pacientes preguntan, con tu tono y revisado antes de salir."),
    ("03 — Cada mes", "Ves a los pacientes llegar", "Un panel simple: cuántas personas te encontraron y cuántas escribieron por WhatsApp."),
]


def cargar(raiz):
    out = []
    for p in sorted((raiz / "_agencia" / "paginas").glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            sys.exit(f"ERROR {p.name}: JSON inválido ({err})")
        faltan = [c for c in ("tipo", "titulo", "meta", "h1", "sub", "wa", "fecha") if not d.get(c)]
        if faltan:
            sys.exit(f"ERROR {p.name}: faltan campos {faltan}")
        d["slug"] = p.stem
        d.setdefault("modificado", d["fecha"])
        d["ruta"] = f"/casos/{p.stem}/" if d["tipo"] == "caso" else f"/{p.stem}/"
        out.append(d)
    return out


def render(pg, arts, h):
    """h = módulo build (para reutilizar cabeza, NAV, FOOTER, JS, e, wa, ld, tarjeta)."""
    e, wa = h.e, h.wa
    url = h.DOMINIO + pg["ruta"]
    porslug = {a["slug"]: a for a in arts}
    guias = [porslug[s] for s in pg.get("guias", []) if s in porslug][:3]
    faq = pg.get("faq") or []
    fuentes = pg.get("fuentes") or []
    link_wa = wa(pg["wa"])

    esquemas = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": h.DOMINIO + "/"},
            {"@type": "ListItem", "position": 2, "name": pg["h1"], "item": url}]},
    ]
    if pg["tipo"] == "caso":
        esquemas.append({"@context": "https://schema.org", "@type": "Article", "headline": pg["h1"], "description": pg["meta"],
                         "datePublished": pg["fecha"], "dateModified": pg["modificado"], "inLanguage": "es-CO",
                         "author": {"@type": "Organization", "name": "Visibla"}, "mainEntityOfPage": url})
    else:
        srv = {"@context": "https://schema.org", "@type": "Service", "name": pg["h1"], "description": pg["meta"],
               "serviceType": "Posicionamiento SEO para clínicas", "url": url,
               "provider": {"@type": "Organization", "name": "Visibla", "url": h.DOMINIO + "/",
                            "telephone": "+57 320 363 8223"}}
        srv["areaServed"] = {"@type": "City", "name": pg["ciudad"]} if pg.get("ciudad") else {"@type": "Country", "name": "Colombia"}
        esquemas.append(srv)
    if faq:
        esquemas.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]})
    extra = "\n".join(h.ld(s) for s in esquemas)

    dolores = "".join(f'<div class="lp-card"><span class="lp-n mono">0{i+1}</span><h3>{e(d["t"])}</h3><p>{e(d["p"])}</p></div>'
                      for i, d in enumerate(pg.get("dolores", [])))
    incluye = "".join(f'<div class="lp-inc"><h3>{e(d["t"])}</h3><p>{e(d["p"])}</p></div>' for d in pg.get("incluye", []))
    pasos = "".join(f'<div class="lp-step"><div class="mono">{a}</div><h3>{b}</h3><p>{c}</p></div>' for a, b, c in PASOS)

    sec_dolores = f"""<section class="lp-sec wrap"><div class="mono lp-k">Lo que pasa hoy</div>
  <div class="lp-grid3">{dolores}</div></section>""" if dolores else ""
    sec_incluye = f"""<section class="lp-sec wrap"><div class="mono lp-k">Qué hacemos por tu clínica</div>
  <h2 class="lp-h2">Un equipo de agentes trabajando por ti cada mañana.</h2>
  <div class="lp-grid2">{incluye}</div></section>""" if incluye else ""
    sec_caso = "" if pg["tipo"] == "caso" else f"""<section class="lp-sec wrap"><a class="lp-caso grain" href="/casos/seravena/">
  <div class="mono">Caso real · Medellín</div>
  <h3>Clínica Seravena: un blog que publica solo cada mañana desde julio de 2026.</h3>
  <div class="lp-stats"><div><b>4,9</b><span>en Google</span></div><div><b>+65</b><span>artículos publicados</span></div><div><b>~55</b><span>contactos por WhatsApp al mes entre web y anuncios</span></div></div>
  <span class="lp-more">Ver el caso completo →</span></a></section>"""
    sec_guias = ""
    if guias:
        sec_guias = '<section class="rel wrap"><div class="mono">Guías relacionadas</div><div class="grid">' + "".join(h.tarjeta(a) for a in guias) + "</div></section>"
    faq_html = ""
    if faq:
        faq_html = '<section class="faq art" style="padding-top:0"><h2>Preguntas frecuentes</h2>' + "".join(
            f"<details><summary>{e(f['q'])}</summary><p>{e(f['a'])}</p></details>" for f in faq) + "</section>"
    fuentes_html = ""
    if fuentes:
        fuentes_html = '<section class="fuentes art" style="padding-top:0"><div class="mono">Fuentes</div><ol>' + "".join(
            f'<li><a href="{e(f["u"])}" target="_blank" rel="noopener nofollow">{e(f["t"])}</a></li>' for f in fuentes) + "</ol></section>"

    return h.cabeza(pg["titulo"] + " | Visibla", pg["meta"], url, extra) + h.NAV.format(wa=link_wa) + f"""
<header class="art-head grain lp-head">
  <div class="blob b1"></div><div class="blob b2"></div><div class="frost"></div>
  <div class="art-head-in">
    <div class="crumbs mono"><a href="/">Inicio</a> / {e(pg.get('kicker', ''))}</div>
    <h1>{e(pg['h1'])}</h1>
    <p class="lead">{e(pg['sub'])}</p>
    <div class="lp-ctas">
      <a class="btn" href="{link_wa}" target="_blank" rel="noopener">Hablar por WhatsApp <span class="ar">→</span></a>
      <a class="btn ghost" href="/diagnostico/">Diagnóstico gratis de mi web</a>
    </div>
  </div>
</header>
{sec_dolores}
<main class="art"><article class="prosa">
{pg.get('contexto', '')}
</article></main>
{sec_incluye}
<section class="lp-sec wrap"><div class="mono lp-k">Cómo trabajamos</div><div class="lp-grid3">{pasos}</div></section>
{sec_caso}
{faq_html}
<div class="art" style="padding-top:0">{h.cta_box({'titulo': pg['h1']}, "Hagamos visible tu clínica.", "Una conversación corta por WhatsApp: revisamos tu web, tu ficha de Google y tus reseñas, y te decimos por dónde empezar.", "Escribir por WhatsApp").replace(h.wa("Hola Visibla, leí la guía «" + pg['h1'] + "» y quiero mi diagnóstico SEO gratis"), link_wa)}</div>
{fuentes_html}
{sec_guias}
{h.FOOTER.format(anio=date.today().year)}
{h.JS}
</body>
</html>
"""


def generar(raiz, arts, h):
    pags = cargar(raiz)
    for pg in pags:
        d = raiz / pg["ruta"].strip("/")
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render(pg, arts, h), encoding="utf-8")
    return pags
