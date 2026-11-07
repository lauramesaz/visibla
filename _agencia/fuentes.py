#!/usr/bin/env python3
"""Fuentes de la web servidas desde posicion-seo.com (antes venían de fonts.googleapis.com).

Toma _agencia/fuentes/Geist.ttf y GeistMono.ttf (variables, licencia SIL OFL 1.1, que va dentro de cada archivo)
y deja en /fuentes/ dos woff2 con solo los caracteres latinos que usa la web:
  geist.woff2       pesos 300 a 700
  geist-mono.woff2  pesos 400 y 500
Los @font-face y el reemplazo ajustado ('Geist Fallback') están en FUENTES_CSS de build.py
y copiados a mano en index.html, plan-seo/ y diagnostico/.

Uso: python3 _agencia/fuentes.py
"""
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI.parent / "fuentes"
LATIN = [*range(0x00, 0x100), 0x131, 0x152, 0x153, 0x2BB, 0x2BC, 0x2C6, 0x2DA, 0x2DC, *range(0x2000, 0x2070),
         0x20AC, 0x2122, *range(0x2190, 0x219A), 0x2212, 0x2215, 0x2248, 0x2260, 0x2264, 0x2265, 0xFEFF, 0xFFFD]
FUENTES = [("Geist.ttf", "geist.woff2", (300, 700)), ("GeistMono.ttf", "geist-mono.woff2", (400, 500))]


def main():
    SALIDA.mkdir(exist_ok=True)
    for origen, destino, pesos in FUENTES:
        f = TTFont(AQUI / "fuentes" / origen, lazy=False)
        op = subset.Options()
        op.layout_features, op.name_IDs, op.name_languages = ["*"], ["*"], ["*"]
        op.notdef_outline, op.hinting = True, False
        s = subset.Subsetter(options=op)
        s.populate(unicodes=LATIN)
        s.subset(f)
        buf = io.BytesIO()
        f.save(buf)
        buf.seek(0)
        f = instancer.instantiateVariableFont(TTFont(buf, lazy=False), {"wght": pesos})
        f.flavor = "woff2"
        f.save(SALIDA / destino)
        print(f"{destino}: {(SALIDA / destino).stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
