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
INSTITUCIONAL = RAIZ / "_agencia" / "institucional"
DOMINIO = "https://posicion-seo.com"
ORG_ID = DOMINIO + "/#org"
# La organización tal como la ve Google en cada página (misma @id que el inicio)
ORG = {"@type": "Organization", "@id": ORG_ID, "name": "Visibla", "alternateName": "posicion-seo.com",
       "url": DOMINIO + "/", "logo": {"@type": "ImageObject", "url": DOMINIO + "/og.png", "width": 1200, "height": 630}}


def cargar_autora():
    """Si existe _agencia/autora.json, las guías van firmadas por esa persona (si no, por el equipo)."""
    p = RAIZ / "_agencia" / "autora.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


AUTORA = cargar_autora()

# Página de venta a la que lleva cada guía al final (si existe); el resto lleva al inicio
VENTA = {
    "seo-clinicas-esteticas": "/agencia-seo-clinicas-esteticas/",
    "fotos-antes-despues-clinica": "/seo-cirujanos-plasticos/",
    "publicidad-servicios-salud-colombia": "/seo-cirujanos-plasticos/",
    "directorios-medicos-seo": "/seo-medicos/",
    "seo-fisioterapia": "/seo-traumatologos/",
    "cuanto-tarda-el-seo": "/plan-seo/",
    "seo-vs-google-ads-clinicas": "/plan-seo/",
    "valor-de-un-paciente": "/plan-seo/",
    "como-elegir-agencia-seo-clinica": "/plan-seo/",
}
PILAR = "seo-para-clinicas"


def portada(ruta_rel, titulo, kicker):
    """URL de la portada propia (1200×630), o la genérica og.png si no se pudo crear."""
    try:
        import portadas
        if portadas.asegurar(RAIZ, ruta_rel, titulo, kicker):
            return f"{DOMINIO}/{ruta_rel}"
    except Exception as err:
        print(f"aviso: sin portada para {ruta_rel} ({err})")
    return f"{DOMINIO}/og.png"
WA = "573203638223"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
CAMPOS = ["titulo", "meta", "fecha", "categoria", "lectura", "resumen"]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap" media="print" onload="this.media=\'all\'">\n'
         '<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap"></noscript>')


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
    <div>SEO con agentes de IA para clínicas · Colombia · © {anio} · <a href="/blog/">Guías</a> · <a href="/diagnostico/">Diagnóstico gratis</a></div>
  </div>
  {{links}}
</footer>"""

JS = """<script>
const nav=document.getElementById('nav'),bar=document.getElementById('progress');
addEventListener('scroll',()=>{const h=document.documentElement;bar.style.transform='scaleX('+(h.scrollTop/(h.scrollHeight-h.clientHeight||1))+')'},{passive:true});
</script>"""


def cabeza(titulo, meta, url, extra="", imagen=None, tipo="article"):
    if titulo.endswith(" | Visibla") and len(titulo) > 60:
        titulo = titulo[:-len(" | Visibla")]  # Google corta los títulos de más de ~60 caracteres
    imagen = imagen or f"{DOMINIO}/og.png"
    return f"""<!DOCTYPE html>
<html lang="es-CO">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(meta)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{tipo}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(meta)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Visibla">
<meta property="og:locale" content="es_CO">
<meta property="og:image" content="{imagen}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(titulo)}">
<meta name="twitter:card" content="summary_large_image">
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


RUTAS_VENTA = {}  # ruta -> nombre corto de las páginas de venta que existen (lo llena main)


def siguiente_paso(a):
    """Enlace al final de cada guía hacia la página que vende ese servicio (o al inicio)."""
    ruta = VENTA.get(a["slug"])
    partes = []
    if ruta and ruta in RUTAS_VENTA and ruta != "/plan-seo/":
        partes.append(f'nuestro servicio de <a href="{ruta}">{e(RUTAS_VENTA[ruta])}</a>')
    partes.append('cómo trabajamos como <a href="/">agencia SEO para clínicas</a>')
    partes.append('el <a href="/plan-seo/">plan SEO de 90 días con precio fijo</a>')
    return ('<p class="siguiente">¿Prefieres que lo hagamos por ti? Mira ' + ", ".join(partes[:-1]) +
            " o " + partes[-1] + ".</p>")


def caja_autora():
    if not AUTORA:
        return ""
    return f"""<aside class="autora">
  <div class="mono">Sobre la autora</div>
  <p><a href="/quienes-somos/"><strong>{e(AUTORA['nombre'])}</strong></a> · {e(AUTORA['cargo'])}. {e(AUTORA['bio_corta'])}</p>
</aside>"""


def pagina_articulo(a, todos):
    url = f"{DOMINIO}/blog/{a['slug']}/"
    cuerpo, indice = toc(a["cuerpo"])
    cuerpo = insertar_cta(cuerpo, a)
    faq = a.get("faq") or []
    fuentes = a.get("fuentes") or []
    pilar = [b for b in todos if b["slug"] == PILAR and a["slug"] != PILAR]
    rel = pilar + [b for b in todos if b["slug"] not in (a["slug"], PILAR) and b["categoria"] == a["categoria"]]
    rel += [b for b in todos if b["slug"] != a["slug"] and b not in rel]
    rel = rel[:3]
    img = portada(f"blog/{a['slug']}/portada.jpg", a["titulo"], a["categoria"])
    if AUTORA:
        autor = {"@type": "Person", "@id": DOMINIO + "/quienes-somos/#" + AUTORA["id"], "name": AUTORA["nombre"],
                 "url": DOMINIO + "/quienes-somos/", "jobTitle": AUTORA["cargo"], "worksFor": {"@id": ORG_ID}}
        firma = f'<a href="/quienes-somos/">{e(AUTORA["nombre"])}</a>'
    else:
        autor, firma = {"@type": "Organization", "name": "Equipo Visibla", "url": DOMINIO + "/"}, "Equipo Visibla"

    esquemas = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titulo"],
         "description": a["meta"], "datePublished": a["fecha"], "dateModified": a["modificado"],
         "inLanguage": "es-CO", "mainEntityOfPage": url,
         "author": autor, "publisher": ORG,
         "image": {"@type": "ImageObject", "url": img, "width": 1200, "height": 630},
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

    return cabeza(a["titulo"] + " | Visibla", a["meta"], url, extra, img) + NAV.format(
        wa=wa("Hola Visibla, quiero agendar una llamada")) + f"""
<header class="art-head grain">
  <div class="blob b1"></div><div class="blob b2"></div><div class="frost"></div>
  <div class="art-head-in">
    <div class="crumbs mono"><a href="/">Inicio</a> / <a href="/blog/">Guías</a> / {e(a['categoria'])}</div>
    <h1>{e(a['titulo'])}</h1>
    <p class="lead">{e(a['resumen'])}</p>
    <div class="meta mono">{firma} · {fecha_larga(a['fecha'])}{act} · {a['lectura']} min de lectura</div>
  </div>
</header>
<main class="art">
  {indice}
  <article class="prosa">
{cuerpo}
  </article>
  {faq_html}
  {caja_autora()}
  {siguiente_paso(a)}
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
  <h2 class="lp-k mono" style="margin-bottom:14px">Todas las guías de SEO para clínicas</h2>
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
    <h2 class="guias-h">Guías de SEO para clínicas: lo que aprendemos posicionándolas.</h2>
    <div class="guias-grid">
{chr(10).join(tarjeta(a) for a in arts[:3])}
    </div>
    <a class="btn ghost" href="/blog/">Ver todas las guías <span class="ar">→</span></a>
  </div>
</section>
<!--BLOG:FIN-->"""


# Landing /plan-seo/ (HTML a mano, con precios): ruta, texto del enlace, fecha de su última edición (cambiarla al editarla)
PLAN_SEO = ("/plan-seo/", "Plan SEO de 90 días", "2026-10-27")


def cargar_institucional():
    """Páginas fijas de la marca (quiénes somos, contacto, privacidad): _agencia/institucional/<slug>.html
    con cabecera JSON {titulo, meta, h1, sub, corto, tipo (AboutPage|ContactPage|WebPage), orden, fecha, modificado}."""
    out = []
    for p in sorted(INSTITUCIONAL.glob("*.html")) if INSTITUCIONAL.exists() else []:
        m = re.match(r"\s*<!--(.*?)-->(.*)", p.read_text(encoding="utf-8"), re.S)
        if not m:
            sys.exit(f"ERROR institucional/{p.name}: falta la cabecera JSON")
        d = json.loads(m.group(1))
        faltan = [c for c in ("titulo", "meta", "h1", "corto", "fecha") if not d.get(c)]
        if faltan:
            sys.exit(f"ERROR institucional/{p.name}: faltan campos {faltan}")
        d.update(slug=p.stem, ruta=f"/{p.stem}/", cuerpo=m.group(2).strip())
        d.setdefault("modificado", d["fecha"])
        out.append(d)
    return sorted(out, key=lambda d: d.get("orden", 9))


def pagina_institucional(d):
    url = DOMINIO + d["ruta"]
    img = portada(f"{d['slug']}/portada.jpg", d["h1"], "Visibla")
    pagina = {"@context": "https://schema.org", "@type": d.get("tipo", "WebPage"), "name": d["h1"], "url": url,
              "description": d["meta"], "inLanguage": "es-CO", "dateModified": d["modificado"],
              "isPartOf": {"@type": "WebSite", "@id": DOMINIO + "/#web"}, "about": {"@id": ORG_ID}}
    esquemas = [pagina, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": DOMINIO + "/"},
        {"@type": "ListItem", "position": 2, "name": d["corto"], "item": url}]}]
    if d.get("tipo") == "AboutPage":
        org = dict(ORG, **{"@context": "https://schema.org", "description": d["meta"],
                          "areaServed": {"@type": "Country", "name": "Colombia"},
                          "telephone": "+57 320 363 8223"})
        if AUTORA:
            persona = {"@type": "Person", "@id": DOMINIO + "/quienes-somos/#" + AUTORA["id"], "name": AUTORA["nombre"],
                       "jobTitle": AUTORA["cargo"], "url": url, "worksFor": {"@id": ORG_ID},
                       "knowsAbout": AUTORA.get("sabe_de", [])}
            org["founder"] = persona
            pagina["mainEntity"] = persona
        esquemas.append(org)
    if d.get("tipo") == "ContactPage":
        pagina["mainEntity"] = {"@id": ORG_ID, "@type": "Organization", "name": "Visibla",
                                "contactPoint": {"@type": "ContactPoint", "telephone": "+57 320 363 8223",
                                                 "contactType": "sales", "availableLanguage": "es", "areaServed": "CO"}}
    sub = f'<p class="lead">{e(d["sub"])}</p>' if d.get("sub") else ""
    return cabeza(d["titulo"] + " | Visibla", d["meta"], url, "\n".join(ld(s) for s in esquemas), img, "website") + NAV.format(
        wa=wa("Hola Visibla, quiero agendar una llamada")) + f"""
<header class="art-head grain">
  <div class="blob b1"></div><div class="blob b2"></div><div class="frost"></div>
  <div class="art-head-in">
    <div class="crumbs mono"><a href="/">Inicio</a> / {e(d['corto'])}</div>
    <h1>{e(d['h1'])}</h1>
    {sub}
  </div>
</header>
<main class="art inst">
  <article class="prosa">
{d['cuerpo']}
  </article>
  {cta_box({'titulo': d['h1']}, "Hagamos visible tu clínica.", "Una conversación corta por WhatsApp: revisamos tu web, tu ficha de Google y tus reseñas, y te decimos por dónde empezar.", "Escribir por WhatsApp").replace(wa("Hola Visibla, leí la guía «" + d['h1'] + "» y quiero mi diagnóstico SEO gratis"), wa("Hola Visibla, quiero hablar con ustedes"))}
</main>
{FOOTER.format(anio=date.today().year)}
{JS}
</body>
</html>
"""


INST = []  # páginas institucionales cargadas (las llena main)


def enlaces_footer(pags):
    grupos = [("Especialidades", "especialidad"), ("Ciudades", "ciudad"), ("Casos", "caso")]
    cols = []
    for nombre, tipo in grupos:
        items = [p for p in pags if p["tipo"] == tipo]
        if items:
            cols.append(f'<div><div class="mono">{nombre}</div>' + "".join(
                f'<a href="{p["ruta"]}">{e(p.get("corto") or p["h1"])}</a>' for p in items) + "</div>")
    # landing de venta hecha a mano (no sale de paginas/*.json)
    cols.append(f'<div><div class="mono">Precios</div><a href="{PLAN_SEO[0]}">{PLAN_SEO[1]}</a></div>')
    if INST:
        cols.append('<div><div class="mono">Visibla</div>' + "".join(
            f'<a href="{d["ruta"]}">{e(d["corto"])}</a>' for d in INST) + '<a href="/blog/">Guías</a></div>')
    return f'<div class="wrap foot-links">{"".join(cols)}</div>' if cols else ""


def sobre_visibla(pags):
    """Bloque para llms.txt: quién es Visibla, sin dejar lugar a confusiones con marcas parecidas."""
    casos = [p for p in pags if p["tipo"] == "caso" and p.get("cliente")]
    lineas = [
        "- Nombre: Visibla (con «a» al final). Su web es posicion-seo.com: el dominio no es el nombre de la marca.",
        "- Qué es: agencia colombiana de SEO para clínicas y médicos (estética, cirugía plástica, vascular, dermatología, "
        "odontología y más). Trabaja de forma remota con clínicas de toda Colombia.",
        "- Cómo trabaja: un equipo de agentes de IA investiga lo que buscan los pacientes, escribe, edita, verifica lo médico "
        "y publica cada mañana; además cuida la ficha de Google y las reseñas, y mide cuántas personas escriben por WhatsApp.",
    ]
    if AUTORA:
        lineas.append(f"- Fundadora: {AUTORA['nombre']}, {AUTORA['cargo']}. {AUTORA['bio_corta']} ({DOMINIO}/quienes-somos/)")
    if casos:
        lineas.append("- Clínicas con caso publicado: " + "; ".join(
            f"{p['cliente']['nombre']} ({p['cliente']['url']}, caso en {DOMINIO}{p['ruta']})" for p in casos) + ".")
    lineas.append("- Contacto: WhatsApp +57 320 363 8223 (https://wa.me/573203638223).")
    return "## Sobre Visibla\n\n" + "\n".join(lineas) + "\n\n"


def main():
    global FOOTER, INST
    import paginas
    arts = cargar()
    INST = cargar_institucional()
    previas = paginas.cargar(RAIZ)
    RUTAS_VENTA.update({p["ruta"]: ("SEO para " + p["corto"].lower()) if p["tipo"] == "especialidad" and p.get("corto")
                        else p["h1"].split(":")[0] for p in previas if p["tipo"] != "caso"})
    FOOTER = FOOTER.replace("{{links}}", enlaces_footer(previas))
    for a in arts:
        d = RAIZ / "blog" / a["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(pagina_articulo(a, arts), encoding="utf-8")
    (RAIZ / "blog" / "index.html").write_text(pagina_listado(arts), encoding="utf-8")
    for d in INST:
        (RAIZ / d["slug"]).mkdir(parents=True, exist_ok=True)
        (RAIZ / d["slug"] / "index.html").write_text(pagina_institucional(d), encoding="utf-8")

    home = RAIZ / "index.html"
    h = home.read_text(encoding="utf-8")
    if "<!--BLOG:INICIO-->" in h:
        h = re.sub(r"<!--BLOG:INICIO-->.*?<!--BLOG:FIN-->", lambda _: bloque_home(arts), h, flags=re.S)
        home.write_text(h, encoding="utf-8")

    pags = paginas.generar(RAIZ, arts, sys.modules[__name__])
    if "<!--PAGINAS:INICIO-->" in h:
        h = re.sub(r"<!--PAGINAS:INICIO-->.*?<!--PAGINAS:FIN-->", lambda _: "<!--PAGINAS:INICIO-->" + enlaces_footer(pags) + "<!--PAGINAS:FIN-->", h, flags=re.S)
        home.write_text(h, encoding="utf-8")

    hoy = date.today().isoformat()
    ult = max([a["modificado"] for a in arts] or [hoy])
    urls = [(f"{DOMINIO}/", ult), (f"{DOMINIO}/blog/", ult)] + [(f"{DOMINIO}/blog/{a['slug']}/", a["modificado"]) for a in arts] + \
        [(DOMINIO + p["ruta"], p["modificado"]) for p in pags] + [(DOMINIO + d["ruta"], d["modificado"]) for d in INST] + \
        [(f"{DOMINIO}/diagnostico/", ult), (DOMINIO + PLAN_SEO[0], PLAN_SEO[2])]
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc><lastmod>{m}</lastmod></url>\n" for u, m in urls) + "</urlset>\n", encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    (RAIZ / "llms.txt").write_text(
        "# Visibla\n\n> Agencia de SEO con agentes de IA para clínicas en Colombia (web: posicion-seo.com). Publica contenido diario revisado, "
        "cuida la ficha de Google y las reseñas, y mide los contactos por WhatsApp. Contacto: WhatsApp +57 320 363 8223.\n\n" +
        sobre_visibla(pags) +
        f"## Páginas principales\n\n- [Inicio: agencia SEO para clínicas]({DOMINIO}/)\n- [Guías de SEO para clínicas]({DOMINIO}/blog/)\n- [Diagnóstico SEO gratis]({DOMINIO}/diagnostico/)\n"
        f"- [Plan SEO de 90 días para clínicas, con precios]({DOMINIO}{PLAN_SEO[0]}): solo SEO desde $500.000 el primer mes y $300.000 los meses 2 y 3; "
        "SEO + gestión de Google Ads desde $1.500.000 el primer mes y $900.000 los meses 2 y 3 (pesos colombianos; la inversión en anuncios va aparte).\n" +
        "".join(f"- [{d['h1']}]({DOMINIO}{d['ruta']}): {d['meta']}\n" for d in INST) +
        "\n## Servicios y casos\n\n" +
        "".join(f"- [{p['h1']}]({DOMINIO}{p['ruta']}): {p['meta']}\n" for p in pags) + "\n## Guías\n\n" +
        "".join(f"- [{a['titulo']}]({DOMINIO}/blog/{a['slug']}/): {a['resumen']}\n" for a in arts), encoding="utf-8")
    print(f"OK · {len(arts)} artículos · {len(pags)} páginas · {len(INST)} institucionales · sitemap con {len(urls)} URLs")


if __name__ == "__main__":
    main()
