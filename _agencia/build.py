#!/usr/bin/env python3
"""Genera el blog de Visibla a partir de _agencia/articulos/*.html.

Cada artículo fuente empieza con un comentario JSON (cabecera) y sigue el cuerpo en HTML:

<!--
{"titulo": "...", "meta": "...", "fecha": "2026-10-02", "modificado": "2026-10-02",
 "categoria": "SEO local", "lectura": 7, "resumen": "...", "keyword": "...",
 "faq": [{"q": "...", "a": "..."}], "fuentes": [{"t": "...", "u": "https://..."}]}
-->
<p>Cuerpo con <h2>, <p>, <ul>, <ol>, <table>, <blockquote> ...</p>

Salida (no editar a mano, se regenera):
  blog/<slug>/index.html   una página por artículo (URL limpia /blog/<slug>/)
  blog/index.html          listado con filtro por categoría
  index.html               bloque "Guías" entre <!--BLOG:INICIO--> y <!--BLOG:FIN-->
  sitemap.xml, robots.txt, llms.txt

Uso: python3 _agencia/build.py
"""
import html, json, re, sys, urllib.parse
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = RAIZ / "_agencia" / "articulos"
DOMINIO = "https://posicion-seo.com"
WA = "573203638223"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
CAMPOS = ["titulo", "meta", "fecha", "categoria", "lectura", "resumen"]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600'
         '&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">')


def wa(texto):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(texto)


def fecha_larga(f):
    a, m, d = map(int, f.split("-"))
    return f"{d} de {MESES[m - 1]} de {a}"


def e(t):
    return html.escape(str(t), quote=True)


def cargar():
    arts = []
    for p in sorted(FUENTES.glob("*.html")):
        txt = p.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--(.*?)-->(.*)", txt, re.S)
        if not m:
            sys.exit(f"ERROR {p.name}: falta la cabecera JSON")
        try:
            cab = json.loads(m.group(1))
        except json.JSONDecodeError as err:
            sys.exit(f"ERROR {p.name}: cabecera JSON inválida ({err})")
        faltan = [c for c in CAMPOS if not cab.get(c)]
        if faltan:
            sys.exit(f"ERROR {p.name}: faltan campos {faltan}")
        cab["slug"] = p.stem
        cab.setdefault("modificado", cab["fecha"])
        cab["cuerpo"] = m.group(2).strip()
        if cab["fecha"] > date.today().isoformat():
            continue  # programado para el futuro
        arts.append(cab)
    arts.sort(key=lambda a: (a["fecha"], a["slug"]), reverse=True)
    return arts


NAV = """<div class="progress" id="progress"></div>
<nav id="nav" class="solid">
  <div class="wrap">
    <a href="/" class="logo"><i></i>Visibla</a>
    <div class="links">
      <a href="/#como">Cómo funciona</a>
      <a href="/#planes">Planes</a>
      <a href="/blog/">Guías</a>
    </div>
    <a href="{wa}" target="_blank" rel="noopener" class="btn">Agendar llamada</a>
  </div>
</nav>"""

FOOTER = """<footer>
  <div class="wrap">
    <a href="/" class="logo" style="font-size:15px;color:var(--ink)"><i style="width:18px;height:18px"></i>Visibla</a>
    <div>SEO con agentes de IA para clínicas · Colombia · © {anio} · <a href="/blog/">Guías</a></div>
  </div>
</footer>"""

JS = """<script>
const nav=document.getElementById('nav'),bar=document.getElementById('progress');
addEventListener('scroll',()=>{const h=document.documentElement;bar.style.transform='scaleX('+(h.scrollTop/(h.scrollHeight-h.clientHeight||1))+')'},{passive:true});
</script>"""


def cabeza(titulo, meta, url, extra=""):
    return f"""<!DOCTYPE html>
<html lang="es-CO">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(meta)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(meta)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Visibla">
<meta property="og:locale" content="es_CO">
<meta name="twitter:card" content="summary">
{FONTS}
<link rel="stylesheet" href="/blog/blog.css">
{extra}
</head>
<body>
"""


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def cta_box(a, titulo, texto, boton):
    return f"""<aside class="cta-in">
  <div class="mono">Visibla · diagnóstico gratis</div>
  <h3>{titulo}</h3>
  <p>{texto}</p>
  <a class="btn" href="{wa(f"Hola Visibla, leí la guía «{a['titulo']}» y quiero mi diagnóstico SEO gratis")}" target="_blank" rel="noopener">{boton} <span class="ar">→</span></a>
</aside>"""


def insertar_cta(cuerpo, a):
    """CTA suave después del 2.º <h2> (o al 40 % si hay pocos)."""
    caja = cta_box(a, "¿Tu clínica ya aparece cuando la buscan?",
                   "Te mostramos en 20 minutos qué buscan tus pacientes en tu ciudad y quién se los está llevando.",
                   "Quiero mi diagnóstico")
    pos = [m.start() for m in re.finditer(r"<h2", cuerpo)]
    if len(pos) >= 3:
        i = pos[2]
        return cuerpo[:i] + caja + "\n" + cuerpo[i:]
    return cuerpo + "\n" + caja


def toc(cuerpo):
    items, n = [], 0

    def ancla(m):
        nonlocal n
        n += 1
        texto = re.sub(r"<[^>]+>", "", m.group(2))
        slug = re.sub(r"[^a-z0-9]+", "-", texto.lower().translate(str.maketrans("áéíóúñü", "aeiounu"))).strip("-")[:60] or f"s{n}"
        items.append((slug, texto))
        return f'<h2{m.group(1)} id="{slug}">{m.group(2)}</h2>'

    cuerpo = re.sub(r"<h2([^>]*)>(.*?)</h2>", ancla, cuerpo, flags=re.S)
    lista = "".join(f'<li><a href="#{s}">{e(t)}</a></li>' for s, t in items)
    return cuerpo, (f'<div class="toc" role="navigation" aria-label="En esta guía"><div class="mono">En esta guía</div><ol>{lista}</ol></div>' if len(items) >= 3 else "")


def pagina_articulo(a, todos):
    url = f"{DOMINIO}/blog/{a['slug']}/"
    cuerpo, indice = toc(a["cuerpo"])
    cuerpo = insertar_cta(cuerpo, a)
    faq = a.get("faq") or []
    fuentes = a.get("fuentes") or []
    rel = [b for b in todos if b["slug"] != a["slug"] and b["categoria"] == a["categoria"]]
    rel += [b for b in todos if b["slug"] != a["slug"] and b not in rel]
    rel = rel[:3]

    esquemas = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titulo"],
         "description": a["meta"], "datePublished": a["fecha"], "dateModified": a["modificado"],
         "inLanguage": "es-CO", "mainEntityOfPage": url,
         "author": {"@type": "Organization", "name": "Equipo Visibla", "url": DOMINIO + "/"},
         "publisher": {"@type": "Organization", "name": "Visibla", "url": DOMINIO + "/"},
         "about": a.get("keyword", a["categoria"])},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": DOMINIO + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guías", "item": DOMINIO + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": a["titulo"], "item": url}]},
    ]
    if faq:
        esquemas.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]})

    extra = "\n".join(ld(s) for s in esquemas) + f'\n<meta property="article:published_time" content="{a["fecha"]}">' \
        f'\n<meta property="article:modified_time" content="{a["modificado"]}">'

    act = f' · Actualizado el {fecha_larga(a["modificado"])}' if a["modificado"] != a["fecha"] else ""
    faq_html = ""
    if faq:
        faq_html = '<section class="faq"><h2 id="preguntas">Preguntas frecuentes</h2>' + "".join(
            f"<details><summary>{e(f['q'])}</summary><p>{e(f['a'])}</p></details>" for f in faq) + "</section>"
    fuentes_html = ""
    if fuentes:
        fuentes_html = '<section class="fuentes"><div class="mono">Fuentes</div><ol>' + "".join(
            f'<li><a href="{e(f["u"])}" target="_blank" rel="noopener nofollow">{e(f["t"])}</a></li>' for f in fuentes) + "</ol></section>"
    rel_html = ""
    if rel:
        rel_html = '<section class="rel wrap"><div class="mono">Sigue leyendo</div><div class="grid">' + "".join(tarjeta(b) for b in rel) + "</div></section>"

    return cabeza(a["titulo"] + " | Visibla", a["meta"], url, extra) + NAV.format(
        wa=wa("Hola Visibla, quiero agendar una llamada")) + f"""
<header class="art-head grain">
  <div class="blob b1"></div><div class="blob b2"></div><div class="frost"></div>
  <div class="art-head-in">
    <div class="crumbs mono"><a href="/">Inicio</a> / <a href="/blog/">Guías</a> / {e(a['categoria'])}</div>
    <h1>{e(a['titulo'])}</h1>
    <p class="lead">{e(a['resumen'])}</p>
    <div class="meta mono">Equipo Visibla · {fecha_larga(a['fecha'])}{act} · {a['lectura']} min de lectura</div>
  </div>
</header>
<main class="art">
  {indice}
  <article class="prosa">
{cuerpo}
  </article>
  {faq_html}
  {cta_box(a, "Hagamos visible tu clínica.", "Una conversación corta por WhatsApp: revisamos tu web, tu ficha de Google y tus reseñas, y te decimos por dónde empezar.", "Escribir por WhatsApp")}
  {fuentes_html}
</main>
{rel_html}
{FOOTER.format(anio=date.today().year)}
{JS}
</body>
</html>
"""


def tarjeta(a):
    return f"""<a class="post" href="/blog/{a['slug']}/" data-cat="{e(a['categoria'])}">
  <span class="chip">{e(a['categoria'])}</span>
  <h3>{e(a['titulo'])}</h3>
  <p>{e(a['resumen'])}</p>
  <span class="mono when">{fecha_larga(a['fecha'])} · {a['lectura']} min</span>
</a>"""


def pagina_listado(arts):
    url = f"{DOMINIO}/blog/"
    cats = sorted({a["categoria"] for a in arts})
    chips = '<button class="tab on" data-c="">Todas</button>' + "".join(f'<button class="tab" data-c="{e(c)}">{e(c)}</button>' for c in cats)
    esquema = {"@context": "https://schema.org", "@type": "Blog", "name": "Guías de SEO para clínicas · Visibla",
               "url": url, "inLanguage": "es-CO",
               "blogPost": [{"@type": "BlogPosting", "headline": a["titulo"], "url": f"{DOMINIO}/blog/{a['slug']}/",
                             "datePublished": a["fecha"]} for a in arts[:30]]}
    titulo = "Guías de SEO para clínicas en Colombia | Visibla"
    meta = "Guías prácticas para que tu clínica aparezca en Google: ficha de Google, reseñas, contenido médico, medición y más. Escritas para dueños de clínicas."
    return cabeza(titulo, meta, url, ld(esquema)) + NAV.format(wa=wa("Hola Visibla, quiero agendar una llamada")) + f"""
<header class="art-head grain list-head">
  <div class="blob b1"></div><div class="blob b2"></div><div class="frost"></div>
  <div class="art-head-in">
    <div class="mono crumbs">Guías Visibla</div>
    <h1>Que Google encuentre tu clínica, paso a paso.</h1>
    <p class="lead">Guías prácticas para dueños y directores de clínicas en Colombia. Sin tecnicismos, con lo que de verdad trae pacientes.</p>
  </div>
</header>
<main class="wrap listado">
  <div class="tabs" id="tabs">{chips}</div>
  <div class="grid" id="posts">
{chr(10).join(tarjeta(a) for a in arts)}
  </div>
</main>
{FOOTER.format(anio=date.today().year)}
{JS}
<script>
document.getElementById('tabs').addEventListener('click',ev=>{{
  const b=ev.target.closest('.tab');if(!b)return;
  document.querySelectorAll('#tabs .tab').forEach(t=>t.classList.toggle('on',t===b));
  document.querySelectorAll('#posts .post').forEach(p=>p.style.display=(!b.dataset.c||p.dataset.cat===b.dataset.c)?'':'none');
}});
</script>
</body>
</html>
"""


def bloque_home(arts):
    if not arts:
        return ""
    return f"""<!--BLOG:INICIO-->
<section class="guias" id="guias">
  <div class="wrap">
    <div class="mono" style="color:var(--steel-deep)">Guías para clínicas</div>
    <h2 class="guias-h">Lo que aprendemos posicionando clínicas, gratis.</h2>
    <div class="guias-grid">
{chr(10).join(tarjeta(a) for a in arts[:3])}
    </div>
    <a class="btn ghost" href="/blog/">Ver todas las guías <span class="ar">→</span></a>
  </div>
</section>
<!--BLOG:FIN-->"""


def main():
    arts = cargar()
    for a in arts:
        d = RAIZ / "blog" / a["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(pagina_articulo(a, arts), encoding="utf-8")
    (RAIZ / "blog" / "index.html").write_text(pagina_listado(arts), encoding="utf-8")

    home = RAIZ / "index.html"
    h = home.read_text(encoding="utf-8")
    if "<!--BLOG:INICIO-->" in h:
        h = re.sub(r"<!--BLOG:INICIO-->.*?<!--BLOG:FIN-->", lambda _: bloque_home(arts), h, flags=re.S)
        home.write_text(h, encoding="utf-8")

    hoy = date.today().isoformat()
    ult = max([a["modificado"] for a in arts] or [hoy])
    urls = [(f"{DOMINIO}/", ult), (f"{DOMINIO}/blog/", ult)] + [(f"{DOMINIO}/blog/{a['slug']}/", a["modificado"]) for a in arts]
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc><lastmod>{m}</lastmod></url>\n" for u, m in urls) + "</urlset>\n", encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    (RAIZ / "llms.txt").write_text(
        "# Visibla\n\n> Agencia de SEO con agentes de IA para clínicas en Colombia. Publica contenido diario revisado, "
        "cuida la ficha de Google y las reseñas, y mide los contactos por WhatsApp. Contacto: WhatsApp +57 320 363 8223.\n\n"
        f"- [Inicio]({DOMINIO}/)\n- [Guías de SEO para clínicas]({DOMINIO}/blog/)\n\n## Guías\n\n" +
        "".join(f"- [{a['titulo']}]({DOMINIO}/blog/{a['slug']}/): {a['resumen']}\n" for a in arts), encoding="utf-8")
    print(f"OK · {len(arts)} artículos · sitemap con {len(urls)} URLs")


if __name__ == "__main__":
    main()
