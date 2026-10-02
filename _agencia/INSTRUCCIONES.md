# Agencia de redacción de Visibla — INSTRUCCIONES MAESTRAS

> Carpeta privada: empieza con `_` y GitHub Pages (Jekyll) NO la publica. Aquí vive el cerebro.
> Web: https://posicion-seo.com · Repo: lauramesaz/visibla (rama `main`) · Marca: **Visibla** (el dominio se llama posicion-seo.com, la marca NO cambia).

## 0. Para qué existe esto

Visibla vende SEO con agentes de IA **a clínicas** (estética, cirugía plástica, vascular, dermatología, odontología, fisioterapia, nutrición/obesidad, centros médicos) en Colombia.
Este blog NO es para pacientes. Es para **dueños, directores médicos y gerentes de clínicas** que se preguntan cómo conseguir más pacientes desde Google.

Meta única y medible: **que dueños de clínicas encuentren Visibla en Google (y en ChatGPT/AI Overviews) y escriban al WhatsApp +57 320 363 8223.**
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
- Un ejemplo concreto y local (ciudad, barrio, tipo de clínica, búsqueda real).
- Una cifra con fuente enlazada.
- Un error común que vemos y cómo se arregla.
- Una frase de `voz-real.md` si aplica (solo citar lo que esté ahí; nunca inventar testimonios).
- Un paso que el lector puede hacer HOY en 10 minutos.

## 3. Reglas de verdad (innegociables)

1. **Nada de datos inventados.** Toda cifra lleva fuente real enlazada en `fuentes` y debe existir en esa fuente. Si no la encuentras, no pongas la cifra.
2. Datos de Visibla o de clientes: SOLO los de `hechos.md`. No inventes casos, clientes, resultados, testimonios ni precios.
3. Precios de Visibla: NO se publican (Laura no ha decidido). Se puede hablar de rangos del mercado SOLO con fuente.
4. Normas colombianas (publicidad en salud, ética médica, habeas data, Supersalud, INVIMA): citar la norma exacta (número y año) con enlace oficial (funcionpublica.gov.co, secretariasenado.gov.co, minsalud.gov.co, sic.gov.co…). Si no estás seguro, no lo afirmes.
5. Herramientas de Google: describir solo funciones que existen hoy; enlazar la ayuda oficial (support.google.com, developers.google.com).
6. No hablar mal de competidores con nombre propio.
7. No dar consejos médicos. El blog habla de marketing, no de salud.

## 4. SEO de cada artículo

- **Una keyword principal** por artículo (en `keyword`), con intención de dueño de clínica. Ej.: "seo para clínicas estéticas", "cómo aparecer en google maps clínica", "agencia seo clínicas medellín".
- Keyword en: título (al inicio si suena natural), primer párrafo, al menos un H2, meta descripción y slug.
- Título ≤ 60 caracteres (sin contar " | Visibla"). Meta 140–158 caracteres, con beneficio claro.
- Slug corto, en minúsculas, sin tildes ni palabras vacías: `seo-clinicas-esteticas`.
- 1.200–2.000 palabras. Profundidad > relleno.
- Estructura: párrafo de entrada que responde la pregunta en 2–3 frases (para fragmento destacado y para IA) → H2 claros (5–8) → pasos accionables → FAQ de 3–5 preguntas reales (en la cabecera `faq`, NO en el cuerpo).
- Al menos 1 tabla o lista de pasos cuando aporte.
- **Enlaces internos:** 2–4 a otras guías publicadas (`/blog/<slug>/`) con texto ancla descriptivo + 1 a la home (`/`) o a `/#como`. Solo enlaces que EXISTAN (mira `_agencia/articulos/`).
- **Enlaces externos:** 2–5 a fuentes de autoridad (Google, estudios, normas). Van en el texto Y en `fuentes`.
- **Local:** 1 de cada 3 artículos con foco de ciudad colombiana (ver `temas.md`). Hablar de esa ciudad con datos reales (barrios con clínicas, búsquedas típicas), no cambiar solo el nombre de la ciudad. Nada de páginas puerta copiadas.
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
