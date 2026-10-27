"""Portadas propias (1200×630) para cada guía y página de Visibla.

Las usa build.py como og:image y como imagen del schema. Se regeneran solo si cambia el texto
(el registro vive en _agencia/.portadas.json). Si Pillow no está instalado, build.py sigue con og.png.

Uso directo (prueba): python3 _agencia/portadas.py "Título de prueba" "Categoría" salida.jpg
"""
import hashlib, json, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FUENTE = AQUI / "fuentes" / "Geist.ttf"
MONO = AQUI / "fuentes" / "GeistMono.ttf"
REGISTRO = AQUI / ".portadas.json"
ANCHO, ALTO, MARGEN = 1200, 630, 80
TINTA, GRIS, ACERO = (12, 14, 18), (70, 80, 96), (125, 147, 171)


def _fuente(ruta, tam, peso):
    from PIL import ImageFont
    f = ImageFont.truetype(str(ruta), tam)
    try:
        f.set_variation_by_name(peso)
    except Exception:
        pass
    return f


def _fondo():
    from PIL import Image, ImageDraw, ImageFilter
    img = Image.new("RGB", (ANCHO, ALTO), (236, 239, 244))
    d = ImageDraw.Draw(img)
    # manchas de luz y acero, luego desenfoque fuerte: el mismo aire de og.png
    for (x, y, r, c) in [(1050, 120, 420, (178, 194, 214)), (700, 620, 460, (134, 154, 180)),
                         (120, 600, 380, (160, 176, 198)), (1180, 620, 260, (226, 231, 238)),
                         (200, 40, 300, (244, 246, 249))]:
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    return img.filter(ImageFilter.GaussianBlur(140))


def _partir(texto, fuente, ancho, d):
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if d.textlength(prueba, font=fuente) <= ancho:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


def dibujar(titulo, kicker, salida):
    from PIL import ImageDraw
    img = _fondo()
    d = ImageDraw.Draw(img)
    # logo: círculo con punto + "Visibla"
    cx, cy = MARGEN + 21, 104
    d.ellipse((cx - 21, cy - 21, cx + 21, cy + 21), outline=TINTA, width=3)
    d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=TINTA)
    d.text((MARGEN + 58, cy), "Visibla", font=_fuente(FUENTE, 38, b"SemiBold"), fill=TINTA, anchor="lm")
    # titular: baja de tamaño hasta caber en 3 líneas
    for tam in (66, 60, 54, 48, 44):
        f = _fuente(FUENTE, tam, b"SemiBold")
        lineas = _partir(titulo, f, ANCHO - 2 * MARGEN, d)
        if len(lineas) <= 3:
            break
    alto_linea = int(tam * 1.12)
    y0 = 330 - (len(lineas) * alto_linea) // 2 + 20
    d.text((MARGEN, y0 - 46), kicker.upper(), font=_fuente(MONO, 22, b"Medium"), fill=(78, 98, 124))
    for i, l in enumerate(lineas):
        d.text((MARGEN, y0 + i * alto_linea), l, font=f, fill=TINTA)
    d.text((MARGEN, 540), "posicion-seo.com  ·  SEO para clínicas en Colombia",
           font=_fuente(FUENTE, 28, b"Regular"), fill=GRIS)
    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    img.save(salida, "JPEG", quality=86, optimize=True, progressive=True)


def asegurar(raiz, ruta_rel, titulo, kicker):
    """Crea (o rehace si cambió el texto) raiz/ruta_rel. Devuelve True si hay portada disponible."""
    try:
        import PIL  # noqa: F401
    except ImportError:
        return (Path(raiz) / ruta_rel).exists()
    try:
        reg = json.loads(REGISTRO.read_text(encoding="utf-8"))
    except Exception:
        reg = {}
    huella = hashlib.sha1(f"v1|{titulo}|{kicker}".encode()).hexdigest()[:12]
    destino = Path(raiz) / ruta_rel
    if reg.get(ruta_rel) != huella or not destino.exists():
        dibujar(titulo, kicker, destino)
        reg[ruta_rel] = huella
        REGISTRO.write_text(json.dumps(reg, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
    return True


if __name__ == "__main__":
    dibujar(sys.argv[1], sys.argv[2], sys.argv[3])
