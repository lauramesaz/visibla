# Agente 6 · Publicador y auditor

Solo actúa si: Policía ≥ 8 en el turno 1 y en el turno 2 (control final), Verificador APROBADO y Juez SEO ≥ 85, y esa evidencia está anotada para `registro.md`.

1. `python3 _agencia/build.py` → debe decir OK.
2. Abre `blog/<slug>/index.html` y confirma: título, meta, canonical `https://posicion-seo.com/blog/<slug>/`, JSON-LD BlogPosting + BreadcrumbList (+ FAQPage si hay FAQ), dos CTA de WhatsApp a 573153811567.
3. Confirma que `sitemap.xml` contiene la URL y que la home tiene el bloque de guías actualizado.
4. Actualiza `temas.md` (publicado + fecha; agrega la keyword a `mapa-palabras.md` con su nueva dueña), `cola-mejoras.md` o `humanizados.md` si el trabajo salió de ahí, y `registro.md` (fecha, slug, nota SEO, humanidad turno 1 → turno 2, veredicto del Verificador, estado).
5. Publica: `git add -A && git commit -m "Guía: <título>" && git pull --rebase && git push`.
6. Espera y verifica en vivo con curl: `https://posicion-seo.com/blog/<slug>/` → 200, y `https://posicion-seo.com/sitemap.xml` contiene el slug. Reintenta hasta 5 min.
7. Avisa a Bing/ChatGPT (IndexNow) con la URL nueva y el blog:
   `curl -s -o /dev/null -w '%{http_code}' -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json' -d '{"host":"posicion-seo.com","key":"d50f7f06bd2b4840918f233459192e91","keyLocation":"https://posicion-seo.com/d50f7f06bd2b4840918f233459192e91.txt","urlList":["https://posicion-seo.com/blog/<slug>/","https://posicion-seo.com/blog/","https://posicion-seo.com/"]}'` (200 o 202 = OK). No borres el archivo `d50f7f06bd2b4840918f233459192e91.txt` de la raíz.
8. Si algo falla y no puedes arreglarlo: revierte tu commit (`git revert`), push, y abre una issue en GitHub con etiqueta `agencia` explicando qué pasó.
