#!/usr/bin/env python3
"""Revisión técnica de todo el sitio ya construido (correr después de build.py).

Revisa en cada página publicada: título y descripción (largo y repetidos), un solo H1, canonical a sí misma,
datos estructurados que se puedan leer, enlaces internos que existan, imágenes de portada y peso del HTML.
Con --externos también prueba los enlaces a otras webs (tarda más).

Uso: python3 _agencia/auditoria.py [--externos]
"""
import concurrent.futures as cf, json, re, sys, urllib.request
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://posicion-seo.com"


def paginas():
    for p in sorted(RAIZ.rglob("index.html")):
        rel = p.relative_to(RAIZ)
        if any(parte.startswith((".", "_")) for parte in rel.parts):
            continue
        yield "/" + str(rel.parent).replace(".", "").strip("/") + ("/" if str(rel.parent) != "." else ""), p


def existe(ruta):
    ruta = ruta.split("#")[0].split("?")[0]
    if not ruta or ruta == "/":
        return True
    f = RAIZ / ruta.lstrip("/")
    return f.is_file() or (f / "index.html").is_file()


def main():
    errores, avisos = [], []
    titulos, metas, externos = defaultdict(list), defaultdict(list), defaultdict(set)
    n = 0
    sitemap = (RAIZ / "sitemap.xml").read_text(encoding="utf-8")
    for ruta, p in paginas():
        if f"<loc>{DOMINIO}{ruta}</loc>" not in sitemap:
            avisos.append(f"{ruta}: no está en el sitemap")
        n += 1
        h = p.read_text(encoding="utf-8")
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        t = t.group(1).strip() if t else ""
        m = re.search(r'<meta name="description" content="(.*?)"', h)
        m = m.group(1) if m else ""
        titulos[t].append(ruta)
        metas[m].append(ruta)
        if not t:
            errores.append(f"{ruta}: sin título")
        elif len(t) > 65:
            avisos.append(f"{ruta}: título de {len(t)} caracteres (Google lo corta): {t}")
        if not m:
            errores.append(f"{ruta}: sin descripción")
        elif not 110 <= len(m) <= 165:
            avisos.append(f"{ruta}: descripción de {len(m)} caracteres")
        h1 = re.findall(r"<h1[\s>]", h)
        if len(h1) != 1:
            errores.append(f"{ruta}: {len(h1)} H1")
        c = re.search(r'<link rel="canonical" href="(.*?)"', h)
        if not c or c.group(1) != DOMINIO + ruta:
            errores.append(f"{ruta}: canonical {c.group(1) if c else 'falta'}")
        for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                json.loads(bloque)
            except json.JSONDecodeError as err:
                errores.append(f"{ruta}: datos estructurados rotos ({err})")
        img = re.search(r'<meta property="og:image" content="(.*?)"', h)
        if img and img.group(1).startswith(DOMINIO) and not existe(img.group(1)[len(DOMINIO):]):
            errores.append(f"{ruta}: la imagen {img.group(1)} no existe")
        for href in re.findall(r'href="([^"]+)"', h):
            if href.startswith(("/", DOMINIO)) and not href.startswith("//"):
                destino = href[len(DOMINIO):] if href.startswith(DOMINIO) else href
                if destino.startswith("/blog/blog.css") or destino.endswith((".css", ".png", ".jpg", ".txt", ".xml")):
                    if not existe(destino):
                        errores.append(f"{ruta}: archivo {destino} no existe")
                    continue
                if not existe(destino):
                    errores.append(f"{ruta}: enlace roto {href}")
            elif href.startswith("http") and "fonts.g" not in href and "wa.me" not in href:
                externos[href.replace("&amp;", "&")].add(ruta)
        kb = len(h.encode()) / 1024
        if kb > 200:
            avisos.append(f"{ruta}: HTML de {kb:.0f} KB")
    for t, rs in titulos.items():
        if t and len(rs) > 1:
            errores.append(f"título repetido en {rs}: {t}")
    for m, rs in metas.items():
        if m and len(rs) > 1:
            errores.append(f"descripción repetida en {rs}")

    if "--externos" in sys.argv:
        def probar(u):
            for metodo in ("HEAD", "GET"):
                try:
                    r = urllib.request.urlopen(urllib.request.Request(u, method=metodo, headers={"User-Agent": "Mozilla/5.0 (auditoria Visibla)"}), timeout=15)
                    return u, r.status
                except urllib.error.HTTPError as err:
                    if metodo == "GET":
                        return u, err.code
                except Exception as err:
                    if metodo == "GET":
                        return u, type(err).__name__
            return u, "?"
        with cf.ThreadPoolExecutor(16) as ex:
            for u, st in ex.map(probar, sorted(externos)):
                if st not in (200, 204, 301, 302, 403, 405, 429):
                    avisos.append(f"enlace externo {st}: {u} (en {', '.join(sorted(externos[u]))[:120]})")

    print(f"Páginas revisadas: {n} · enlaces externos: {len(externos)}")
    print(f"\nERRORES ({len(errores)})")
    for x in errores:
        print("  -", x)
    print(f"\nAVISOS ({len(avisos)})")
    for x in avisos:
        print("  -", x)
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
