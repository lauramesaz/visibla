#!/usr/bin/env python3
"""Iconos de Visibla, hechos con la misma marca del menú (.logo i: anillo con punto, tinta #0c0e11).

Genera en la raíz de la web:
  favicon.svg           icono vectorial (pestañas modernas)
  favicon.ico           16, 32 y 48 px (Google pide un múltiplo de 48)
  icon-192.png          icono grande para Android y buscadores
  apple-touch-icon.png  180×180, fondo blanco (iOS no acepta transparencia)
  logo-512.png          logo cuadrado: marca + "Visibla" en negro sobre blanco (logo del schema Organization)

Uso: python3 _agencia/iconos.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
TINTA = (12, 14, 17, 255)
BLANCO = (255, 255, 255, 255)
# Proporciones en una cuadrícula de 32: anillo de radio 13 y trazo 3, punto de radio 6 (las del icono de /plan-seo/)
R_ANILLO, TRAZO, R_PUNTO = 13, 3, 6

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<circle cx="16" cy="16" r="16" fill="#fff"/>
<circle cx="16" cy="16" r="13" fill="none" stroke="#0c0e11" stroke-width="3"/>
<circle cx="16" cy="16" r="6" fill="#0c0e11"/>
</svg>
"""


def marca(lado, fondo="disco", escala=1.0):
    """Dibuja la marca a 8x y la reduce (bordes suaves). fondo: 'disco' (círculo blanco), 'cuadro' (blanco) o None."""
    s = lado * 8
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0) if fondo != "cuadro" else BLANCO)
    d = ImageDraw.Draw(img)
    if fondo == "disco":
        d.ellipse((0, 0, s - 1, s - 1), fill=BLANCO)
    u = s / 32 * escala
    c = s / 2
    ro, ri = (R_ANILLO + TRAZO / 2) * u, (R_ANILLO - TRAZO / 2) * u
    d.ellipse((c - ro, c - ro, c + ro, c + ro), fill=TINTA)
    d.ellipse((c - ri, c - ri, c + ri, c + ri), fill=BLANCO if fondo else (0, 0, 0, 0))
    rp = R_PUNTO * u
    d.ellipse((c - rp, c - rp, c + rp, c + rp), fill=TINTA)
    return img.resize((lado, lado), Image.LANCZOS)


def logo_512():
    s, k = 512, 4
    img = Image.new("RGBA", (s * k, s * k), BLANCO)
    d = ImageDraw.Draw(img)
    fuente = ImageFont.truetype(str(AQUI / "fuentes" / "Geist.ttf"), 112 * k)
    try:
        fuente.set_variation_by_name("Medium")
    except Exception:
        pass
    texto = "Visibla"
    x0, y0, x1, y1 = d.textbbox((0, 0), texto, font=fuente)
    alto_marca = 196 * k
    hueco = 44 * k
    total = alto_marca + hueco + (y1 - y0)
    top = (s * k - total) / 2
    c, u = s * k / 2, alto_marca / 32
    cy = top + alto_marca / 2
    # en grande, el anillo va tan fino como el del menú de la web (borde de 1,5 px en 22 px)
    ro, ri, rp = 14.5 * u, 12.5 * u, R_PUNTO * u
    d.ellipse((c - ro, cy - ro, c + ro, cy + ro), fill=TINTA)
    d.ellipse((c - ri, cy - ri, c + ri, cy + ri), fill=BLANCO)
    d.ellipse((c - rp, cy - rp, c + rp, cy + rp), fill=TINTA)
    ty = top + alto_marca + hueco - y0
    d.text(((s * k - (x1 - x0)) / 2 - x0, ty), texto, font=fuente, fill=TINTA)
    return img.resize((s, s), Image.LANCZOS).convert("RGB")


def main():
    (RAIZ / "favicon.svg").write_text(SVG, encoding="utf-8")
    # cada tamaño dibujado aparte (no reducido desde uno grande) para que el anillo se vea nítido a 16 px
    marca(48, "disco").save(RAIZ / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)],
                            append_images=[marca(16, "disco"), marca(32, "disco")])
    marca(192, "disco").save(RAIZ / "icon-192.png", optimize=True)
    marca(180, "cuadro", escala=0.62).convert("RGB").save(RAIZ / "apple-touch-icon.png", optimize=True)
    logo_512().save(RAIZ / "logo-512.png", optimize=True)
    print("OK · favicon.svg, favicon.ico (16/32/48), icon-192.png, apple-touch-icon.png, logo-512.png")


if __name__ == "__main__":
    main()
