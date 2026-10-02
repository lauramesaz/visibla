# Agente 6 · Publicador y auditor

Solo actúa si: Policía ≥ 8, Verificador APROBADO y Juez SEO ≥ 85.

1. `python3 _agencia/build.py` → debe decir OK.
2. Abre `blog/<slug>/index.html` y confirma: título, meta, canonical `https://posicion-seo.com/blog/<slug>/`, JSON-LD BlogPosting + BreadcrumbList (+ FAQPage si hay FAQ), dos CTA de WhatsApp a 573203638223.
3. Confirma que `sitemap.xml` contiene la URL y que la home tiene el bloque de guías actualizado.
4. Actualiza `temas.md` (publicado + fecha) y `registro.md` (fecha, slug, nota SEO, humanidad, estado).
5. Publica: `git add -A && git commit -m "Guía: <título>" && git pull --rebase && git push`.
6. Espera y verifica en vivo con curl: `https://posicion-seo.com/blog/<slug>/` → 200, y `https://posicion-seo.com/sitemap.xml` contiene el slug. Reintenta hasta 5 min.
7. Si algo falla y no puedes arreglarlo: revierte tu commit (`git revert`), push, y abre una issue en GitHub con etiqueta `agencia` explicando qué pasó.
