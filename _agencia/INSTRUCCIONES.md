# Agencia de redacción de Visibla — INSTRUCCIONES MAESTRAS

> Carpeta privada: empieza con `_` y GitHub Pages (Jekyll) NO la publica. Aquí vive el cerebro.
> Web: https://posicion-seo.com · Repo: lauramesaz/visibla (rama `main`) · Marca: **Visibla** (el dominio se llama posicion-seo.com, la marca NO cambia).

## 0. Para qué existe esto

Visibla vende SEO con agentes de IA **a clínicas** (estética, cirugía plástica, vascular, dermatología, odontología, fisioterapia, nutrición/obesidad, centros médicos) en Colombia.
Este blog NO es para pacientes. Es para **dueños, directores médicos y gerentes de clínicas** que se preguntan cómo conseguir más pacientes desde Google.

Meta única y medible: **que dueños de clínicas encuentren Visibla en Google (y en ChatGPT/AI Overviews) y escriban al WhatsApp +57 315 381 1567.**
Cada artículo es una puerta de entrada: resuelve de verdad una duda del dueño de clínica y, al final, le ofrece el diagnóstico gratis por WhatsApp.

El propio blog es la prueba del producto: si Visibla posiciona su blog, demuestra que sabe posicionar el de una clínica.

## 1. Lector ideal

- Médico o médica dueña de clínica pequeña o mediana (1 a 3 sedes), o gerente/directora comercial.
- Vive en Colombia (Medellín, Bogotá, Cali, Barranquilla, Pereira, Bucaramanga, Cartagena…).
- Hoy consigue pacientes por Instagram, referidos y pauta. Siente que depende de pagar anuncios.
- No es técnico. Le aburre la jerga. Quiere saber **qué hacer, cuánto tarda y qué gana**.
- Tiene poco tiempo: lee en el celular, entre consultas.

## 2. Voz

- Español de Colombia, tuteo, frases cortas. Cálido pero directo, como un colega que sabe del tema.
- Explica con ejemplos de clínicas ("si alguien en Laureles busca 'botox cerca de mí'…").
- Cero jerga sin traducir. Si usas un término (SERP, backlink, E-E-A-T), explícalo en la misma frase o no lo uses.
- Honesto: el SEO tarda meses, no hay garantías de posición, y lo decimos.
- Nada de promesas tipo "primer lugar en 30 días", "garantizado", "100 % seguro".

### 2.1 Huellas de IA PROHIBIDAS (el Policía las caza)
- Rayas largas (—) como muletilla. Máximo 2 en todo el artículo. Mejor usar punto o coma.
- Arranques gastados: "En el mundo actual", "En la era digital", "Hoy en día", "Es importante destacar", "Cabe resaltar", "Sin lugar a dudas", "En conclusión", "En resumen".
- Estructura "no solo… sino también…" más de una vez.
- Tríadas de adjetivos en cadena ("rápido, eficaz y seguro") repetidas.
- Metas que empiezan con pregunta y terminan en "Te contamos". Varía.
- Párrafos que terminan con una moraleja motivacional.
- Listas de 5 viñetas idénticas en forma cuando un párrafo bastaba.

### 2.2 Señales de persona real (al menos 3 por artículo)
- Un dato o caso propio comprobable: de `hechos.md`, de `datos-propios.md` (cuando exista) o una búsqueda real de `search-console.md`. Nunca una clínica inventada como ejemplo principal; si hace falta un caso hipotético, uno solo y rotulado "Ejemplo".
- Una cifra con fuente enlazada.
- Un error común que vemos y cómo se arregla.
- Una frase de `voz-real.md` si aplica (solo citar lo que esté ahí; nunca inventar testimonios).
- Un paso práctico, con otra fórmula cada vez (nunca "Haz esto hoy en 10 minutos" ni un cierre copiado de otra guía).

## 3. Reglas de verdad (innegociables)

1. **Nada de datos inventados.** Toda cifra lleva fuente real enlazada en `fuentes` y debe existir en esa fuente. Si no la encuentras, no pongas la cifra.
2. Datos de Visibla o de clientes: SOLO los de `hechos.md`. No inventes casos, clientes, resultados, testimonios ni precios.
3. Precios de Visibla: SOLO los de `hechos.md` y SOLO en /plan-seo/ (los planes los dos planes de 90 días de /plan-seo/ no tienen precio publicado). En guías y páginas de venta no se repiten cifras: se enlaza a /plan-seo/. Rangos del mercado SOLO con fuente.
4. Normas colombianas (publicidad en salud, ética médica, habeas data, Supersalud, INVIMA): citar la norma exacta (número y año) con enlace oficial (funcionpublica.gov.co, secretariasenado.gov.co, minsalud.gov.co, sic.gov.co…). Si no estás seguro, no lo afirmes. Nunca citar el artículo 57 de la Ley 23 de 1981: es inexequible.
5. Herramientas de Google: describir solo funciones que existen hoy; enlazar la ayuda oficial (support.google.com, developers.google.com).
6. No hablar mal de competidores con nombre propio.
7. No dar consejos médicos. El blog habla de marketing, no de salud.
8. No basar ejemplos en clínicas inventadas. Si hace falta un caso hipotético, uno solo por guía y rotulado "Ejemplo" en el mismo párrafo.
9. No pedirle al lector que desconfíe de cualquiera que le escriba sin que lo pida (Visibla también escribe a clínicas). Si el tema lo necesita: "desconfía de quien te escribe prometiendo posiciones sin mostrarte un diagnóstico real de tu web".

## 4. SEO de cada artículo

- **Mapa de palabras primero:** antes de elegir o cambiar una keyword, búscala en `_agencia/mapa-palabras.md`. Una búsqueda tiene UNA sola página dueña: si ya la tiene, no escribas otra guía para ella; mejora la dueña o enlázala.
- **Una keyword principal** por artículo (en `keyword`), con intención de dueño de clínica. Ej.: "seo para nutricionistas", "cómo aparecer en google maps clínica", "seo para clínicas en medellín" (cada una con su dueña en `mapa-palabras.md`).
- Keyword en: título (al inicio si suena natural), H1 (en el blog el H1 es el título), primer párrafo, al menos un H2, meta descripción y slug.
- Título: máximo 60 caracteres en total. Si con " | Visibla" pasa de 60, `build.py` quita la marca solo.
- Título ≤ 60 caracteres (sin contar " | Visibla"). Meta 140–158 caracteres, con beneficio claro.
- Slug corto, en minúsculas, sin tildes ni palabras vacías: `seo-clinicas-esteticas`.
- 1.200–2.000 palabras. Profundidad > relleno.
- Estructura: párrafo de entrada que responde la pregunta en 2–3 frases (para fragmento destacado y para IA) → H2 claros (5–8) → pasos accionables → FAQ de 3–5 preguntas reales (en la cabecera `faq`, NO en el cuerpo).
- Al menos 1 tabla o lista de pasos cuando aporte.
- **Enlaces internos:** 2–4 a otras guías publicadas (`/blog/<slug>/`) con texto ancla descriptivo + 1 a la home (`/`) o a `/#como`. Solo enlaces que EXISTAN (mira `_agencia/articulos/`).
- **Páginas de venta:** cada guía enlaza UNA vez, dentro del texto, a la página de venta que le da `mapa-palabras.md` (o la columna "Enlaza a" de `temas.md`), con texto natural (ej. "cómo trabajamos con clínicas estéticas" → `/agencia-seo-clinicas-esteticas/`). No escribas artículos que compitan con esas páginas (keyword "agencia SEO + especialidad/ciudad").
- **Enlaces externos:** 2–5 a fuentes de autoridad (Google, estudios, normas). Van en el texto Y en `fuentes`.
- **Dato propio:** cada guía nueva o mejorada lleva al menos 1 dato propio comprobable (de `hechos.md`, `datos-propios.md` o `search-console.md`).
- **Local:** si el tema es de una ciudad (ver `temas.md`), hablar de esa ciudad con datos reales (barrios con clínicas, búsquedas típicas), no cambiar solo el nombre de la ciudad. Nada de páginas puerta copiadas.
- **Lo que dice Google:** antes de elegir tema lee `_agencia/search-console.md` (foto semanal de Search Console que deja el analista de los lunes). Prioriza búsquedas que ya traen apariciones pero no tienen página dueña en `mapa-palabras.md`, y si una guía sale en Google pero nadie la abre, propón mejorar su título y descripción.
- **No canibalizar:** antes de escribir, lee títulos y keywords de `_agencia/articulos/`. Si ya hay uno que apunta a la misma keyword, elige otro tema o propone actualizar ese.
- **Para IA (ChatGPT, AI Overviews):** respuestas directas al inicio de cada H2, definiciones claras, listas de pasos numeradas, FAQ. Así las IA citan el artículo.

## 5. Formato del archivo fuente

Cada artículo es `_agencia/articulos/<slug>.html`:

```
<!--
{
  "titulo": "SEO para clínicas estéticas: guía para llenar la agenda",
  "meta": "Cómo lograr que tu clínica estética aparezca en Google cuando buscan tus tratamientos en tu ciudad. Pasos concretos, tiempos reales y errores comunes.",
  "fecha": "2026-10-02",
  "modificado": "2026-10-02",
  "categoria": "SEO por especialidad",
  "keyword": "seo para clínicas estéticas",
  "lectura": 8,
  "resumen": "Una o dos frases que salen en la tarjeta del listado.",
  "faq": [{"q": "¿Cuánto tarda?", "a": "Respuesta de 2 a 4 frases."}],
  "fuentes": [{"t": "Google · Cómo mejorar tu clasificación local", "u": "https://support.google.com/business/answer/7091"}]
}
-->
<p>Párrafo de entrada…</p>
<h2>…</h2>
…
```

- El cuerpo usa SOLO: `<p> <h2> <h3> <ul> <ol> <li> <strong> <em> <a> <table> <thead> <tbody> <tr> <th> <td> <blockquote>` y `<div class="nota">` para un recuadro.
- NO pongas `<h1>`, FAQ, fuentes, CTA ni índice en el cuerpo: los agrega `build.py` solo (el CTA de WhatsApp va dos veces, automático).
- Categorías permitidas (usa una exacta): `SEO local`, `Google Maps y reseñas`, `Contenido y blog`, `SEO por especialidad`, `SEO por ciudad`, `Medición y resultados`, `IA y buscadores`, `Normas y ética`.
- `lectura` = palabras / 220, redondeado.

## 6. Publicar

1. `python3 _agencia/build.py` (debe decir `OK · N artículos`). Si da ERROR, arréglalo; no publiques roto.
2. Revisa que `blog/<slug>/index.html` existe y que el sitemap lo incluye.
3. Actualiza `temas.md` (estado → publicado + fecha) y añade una línea a `registro.md`.
4. `git add -A && git commit -m "Guía: <título>" && git pull --rebase && git push`.
5. Espera ~60 s y comprueba `https://posicion-seo.com/blog/<slug>/` responde 200 (si aún no, reintenta a los 2 min; GitHub Pages tarda).

## 7. Actualizar en vez de borrar

- Nunca borrar artículos. Si uno queda viejo o flojo: mejorar contenido, cambiar `modificado` a hoy, mantener slug.
- Cambiar `modificado` SOLO si hubo un cambio real de contenido.

## 8. Días de mejora (martes y jueves; también el miércoles 11-nov)

Desde el 9-nov-2026 la agencia publica UNA guía nueva por semana (el lunes) y dedica el resto de la semana a mejorar, reforzar y enlazar lo que ya existe: un sitio nuevo crece más rápido si cada página es más útil que si hay más páginas. Hay 10 guías esperando que Google las guarde.

1. **Cuál mejorar.** No la eliges tú: toma la primera entrada `[pendiente]` de la lista de guías de `_agencia/cola-mejoras.md` que cumpla sus condiciones (fecha "no antes del", no mejorada en los últimos 30 días según `registro.md`). Si la lista de guías se acabó, sigue la sección F de ese archivo.
2. **Qué hacer.** Darle algo que no tenga ninguna otra página sobre el tema: un dato propio de `datos-propios.md` o `hechos.md` (o una búsqueda real de `search-console.md`), una tabla o lista de chequeo propia, pasos exactos con lo que la persona ve en pantalla, datos nuevos con fuente. Si la guía tiene una clínica inventada, cámbiala por ese dato propio o quítala. Si cierra con "Haz esto hoy en 10 minutos", cambia ese cierre por un paso práctico dicho con otras palabras. Respuesta directa en las 2–3 primeras frases y al inicio de cada H2. Recortar lo genérico y lo que repite a otra guía (enlazar a esa guía en su lugar). Revisar enlaces internos: la pilar `/blog/seo-para-clinicas/`, 2–3 guías hermanas y su página de venta según `mapa-palabras.md`. Comprobar que cada fuente sigue abriendo.
3. **Reglas.** Se conserva el slug y la `fecha`; `modificado` = hoy. Si la guía ya sale en Google, no cambies la keyword principal. Todo pasa por el pipeline completo (Policía turno 1, Verificador, Juez SEO, Policía turno 2) igual que una guía nueva.
4. **Registro.** Marca la entrada en `cola-mejoras.md` como `[hecho AAAA-MM-DD · nota SEO · humanidad]`, fila en `registro.md` con "Mejora: <título>" y estado `mejorado`; commit `Mejora: <título>`.

## 9. Miércoles de página de venta (desde el 18-nov-2026)

1. Toma la primera página `[pendiente]` de la lista E de `cola-mejoras.md` (saltando las que no existan todavía en `_agencia/paginas/` o con `modificado` de los últimos 30 días).
2. Solo se tocan TEXTOS de `_agencia/paginas/<slug>.json`: FAQ y párrafos. Nunca precios, estructura, diseño, el orden de los bloques ni los datos de los casos fuera de lo que diga `hechos.md`.
3. Respuesta directa en las 2 primeras frases; FAQ con las búsquedas reales que `mapa-palabras.md` le asigna a esa página; 1 o 2 enlaces a guías que la apoyen. `modificado` = hoy.
4. Pipeline: Redactor → Policía turno 1 → Verificador → Juez SEO → Policía turno 2 → `python3 _agencia/build.py` (genera también las páginas de venta desde `paginas/*.json`) → `python3 _agencia/auditoria.py` → publicar. Registro: estado `reforzado`; commit `Refuerzo: <título>`.

## 10. Viernes: enlazado interno y limpieza

1. **Enlazado (3 guías).** Sigue la sección "Viernes: enlazado interno" de `cola-mejoras.md`: 1 o 2 enlaces por guía, dentro de párrafos que ya existen, hacia su página de venta y hacia guías que aún no están en Google. No cambia `modificado` (§7). El Verificador comprueba que cada enlace exista y que el texto ancla diga la verdad. Registro: estado `enlazado`; commit `Enlazado: <slugs>`.
2. **Limpieza (turno 3 del Policía).** La primera pieza `[pendiente]` de `humanizados.md`, según el manual del Policía. Registro: estado `humanizado`; commit `Humanizado: <título>`.
