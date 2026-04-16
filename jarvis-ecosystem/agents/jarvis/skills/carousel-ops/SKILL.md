---
name: carousel-ops
description: "Carruseles Instagram: narrativa, dimensiones, caption/hashtags, checklist de calidad de diseño (mejor resultado posible en el stack). Pipeline copy + Canva (Composio) hasta export; publicacion AG-03."
---

# Carousel ops (Instagram)

**Qué se toma del proyecto [open-carrusel](https://github.com/Hainrixz/open-carrusel) (MIT):** criterios de diseno, arco narrativo por slides, reglas de HTML seguro, dimensiones IG, caption/hashtags. **Qué se descarta para el ecosistema:** la app Next.js, Puppeteer, Chromium y el chat acoplado a Claude CLI **no** forman parte del repo ni del gateway OpenClaw.

Este skill define **metodologia**, **salidas**, **pipeline Canva** y el **compromiso de calidad de diseño** (seccion siguiente): no garantiza premios de diseno subjetivos, si **maximizar** resultado con brief rico, reglas visuales y practicas alineadas a documentacion oficial Canva / asistentes IA — ver [CAROUSEL_IG_JARVIS.md](../../../../docs/CAROUSEL_IG_JARVIS.md).

## Cuando activar

- `mkt-content` o Jarvis preparan **carrusel Instagram** (campana o cliente con dossier).
- Hace falta **guion estructurado** alineado a marca antes de disenar en Canva/Figma/otra app.
- Complementa [`copywriting-ops`](../copywriting-ops/SKILL.md) cuando el formato es **multi-slide** con gancho y CTA final.

## Brief por red (obligatorio si el humano no lo especifico)

**Logica:** cada red tiene limites de caracteres, ratios y tono distintos; el carrusel con imagenes no es lo mismo que un hilo de X ni un post de LinkedIn. **No asumir** un solo formato para todo.

Si falta **cualquiera** de estos datos, **preguntar primero** (lista corta, una sola ronda) antes de redactar el entregable final:

| Pregunta | Por que importa |
|----------|-----------------|
| **Que red(es)?** (IG, LinkedIn, X, Facebook, TikTok caption, etc.) | Limites de texto, hashtags, tono, si va carrusel o post unico. |
| **Formato?** (carrusel N slides, post unico, story, Reels guion, newsletter) | Estructura y longitud. |
| **Solo copy o tambien diseno?** (Canva / open-carrusel / texto con URLs de imagen) | Si el humano pidio **post IG** o **contenido + diseno**, asumir **pipeline completo** (copy + Canva) salvo que diga explicitamente "solo texto". |
| **Marca y ratio?** (ej. IG 4:5, LinkedIn 1200x627) | Dimensiones y safe zone. |
| **Idioma y CTA?** | Coherencia con campana. |

Si el humano dice **"para IG"** o **"carrusel 6 slides"**, es suficiente; no hace falta repreguntar lo obvio.

## Prerrequisitos

1. Leer [`product-marketing-context.md`](../../../../.agents/product-marketing-context.md) (audiencia, voz, colores si estan declarados).
2. Si hay cliente: dossier en `client-dossiers/` y lineas rojas del encargo.
3. **Publicar** en IG (subir a la red / programar): gate **AG-03** en [APPROVAL_GATES.md](../../../../docs/APPROVAL_GATES.md). **No** confundir con crear/exportar borrador en Canva: AG-03 es para **publicacion** visible.

## Dimensiones Instagram (referencia)

| Ratio | Pixeles | Uso |
|-------|---------|-----|
| 1:1 | 1080 x 1080 | Cuadrado feed |
| 4:5 | 1080 x 1350 | Retrato (recomendado carrusel) |
| 9:16 | 1080 x 1920 | Stories / Reels frame |

Maximo razonable **10 slides** por carrusel; una **idea principal por slide**.

## Arco narrativo (plantilla)

1. **Slide 1 — Hook:** pregunta provocativa, dato contundente o frase contraria (titular corto, max ~8 palabras de gancho).
2. **Slides 2–3 — Contexto:** problema o situacion del lector.
3. **Slides 4–6 — Valor:** un insight por slide, texto breve.
4. **Penultimo — Sintesis** o transformacion.
5. **Ultimo — CTA:** seguir, guardar, compartir, enlace en bio (segun politica del cliente).

## Design intelligence (portable)

Aplica a HTML/CSS manual o a cualquier herramienta visual:

- **Tipografia:** titular hook 64–96px equivalente visual; cuerpo 24–28px; max **2 familias** por carrusel; interlineado 1.2 titulos, 1.5 cuerpo.
- **Contraste:** texto/fondo ratio **> 4.5:1** (WCAG basico).
- **Layout:** padding minimo **60–80px** laterales; contenido critico en **centro ~80%** (crop 1:1 en grid).
- **Color:** primario titulos, acento CTAs, fondo coherente con marca; gradientes suaves mejor que patrones cargados.
- **Movil primero:** el usuario ve el thumb en feed — el hook debe leerse en miniatura.

### Optimizacion de hook (si el primer slide falla)

Proponer **3 variantes**: pregunta, estadistica, afirmacion contraria; el humano elige una.

## Calidad de diseño: compromiso Jarvis-Ecosystem (“el mejor diseno posible” en este stack)

**Significado:** el ecosistema debe **aspirar al mejor resultado alcanzable** con las herramientas conectadas (Composio/Connect/MCP), no prometer “el mejor del mundo” sin revision humana. Eso implica **proceso obligatorio**, no solo ejecutar un `POST` vacio.

### Que hacen Canva y los asistentes (oficial)

Canva documenta para quienes usan **MCP / conector de IA** (Claude, ChatGPT, etc.): prompts **especificos** (dimensiones, estilo, texto, nombre del diseno), **iterar** en varios turnos en lugar de un solo prompt vago, y mantener **carpetas / nombres claros** para que el asistente encuentre disenos — ver [Actions you can take in AI assistants connected to Canva MCP](https://www.canva.com/help/mcp-canva-usage/) (ingles) / [Acciones con Canva MCP](https://www.canva.com/es_us/help/mcp-canva-usage/) (ES). El patron [design edit handoff](https://www.canva.dev/docs/mcp/workflows/design-edit/) exige **siempre** ofrecer enlace para abrir y refinar en el editor.

En integraciones tipo **Claude + Canva**, Canva destaca **Brand Kit** para colores, fuentes y voz coherentes desde el primer borrador — ver [Create on-brand Canva designs directly inside Claude](https://www.canva.com/newsroom/news/claude-ai-connector/) y [AI Connector](https://www.canva.com/es_us/ai-connector/).

### Que hace OpenClaw en la practica

- **Composio + toolkit Canva:** autofill con **brand templates** cuando existan (`CANVA_RETRIEVE_BRAND_TEMPLATE_DATASET_DEFINITION` antes de autofill), crear diseno con **brief rico** (dimensiones, intencion de estilo, assets). Guia plugin: [Composio + OpenClaw](https://composio.dev/toolkits/canva/framework/openclaw).
- **Skill Connect / CLI:** mismas APIs; el operador puede repetir export con parametros distintos.

### Checklist obligatoria del agente antes de dar por bueno un diseno Canva

1. **Brief para la herramienta:** no solo “crea un post”; incluir ratio, tono visual (minimal, contraste alto, foto producto, etc.), colores de marca del dossier o `product-marketing-context`, y texto por capas si la accion lo acepta.
2. **Prioridad:** si hay **brand templates** en la cuenta, **listar → dataset → autofill** antes que lienzo vacio + solo logo.
3. **Design intelligence** de este skill (contraste, jerarquia, movil primero): aplicar como **criterio de revision**; si el export es claramente pobre (solo logo centrado sin jerarquia), **segundo intento** con prompt mas especifico o indicar apertura de `edit_url` para retoque humano rapido.
4. **Handoff:** siempre incluir **Editar en Canva** cuando exista `design_id` o URL devuelta por la API.
5. **Honestidad:** si el plan es gratis y sin brand templates, declarar que el techo es “lienzo + assets”, no plantilla del explorador — ver [CAROUSEL_IG_JARVIS.md](../../../../docs/CAROUSEL_IG_JARVIS.md).

### Anti-patron “diseno horrible” (API sin plantilla de marca)

Un resultado **solo texto negro centrado sobre blanco** (o un logo minusculo sin jerarquia) es **borrador minimo**, no un entregable de marca. Ocurre cuando el agente crea diseno + texto sin **brief visual** ni **segundo paso** (imagen de fondo, color de marca, asset hero).

**Regla:** no dar por **cerrado** un post con diseno si el unico resultado programable es ese anti-patron, **salvo** que en la misma respuesta se diga con claridad: *borrador API minimo — abrir `edit_url` y aplicar estilo en 3–5 minutos* (o se haya intentado subir fondo/logo segun herramientas disponibles).

### Brief visual minimo (cuando NO hay brand template autofill)

Antes de llamar a crear diseno, el agente debe fijar (en prompt a la herramienta o en texto al usuario) **al menos**:

| Campo | Ejemplo |
|-------|---------|
| **Fondo** | Color hex marca o oscuro (#0a0a0a) + texto claro; o intencion “foto producto / textura sutil” si se sube asset |
| **Titular** | Texto exacto + jerarquia (una linea gancho grande; subtitulo opcional mas pequeno) |
| **Logo / imagen** | URL o asset: posicion preferida (esq. sup. izq.) si la API lo admite como capa |
| **Contraste** | Explicito: “WCAG AA titulo sobre fondo” |

Luego: **listar brand templates** si la cuenta puede (`items` no vacio); si hay match, **dataset + autofill** antes que lienzo vacio.

### Iteracion

Si el primer resultado no cumple el checklist, **un turno mas** de refinamiento (otra llamada a herramientas o instrucciones mas detalladas) antes de cerrar; coherente con Canva Help (refinar por chat).

Si tras el primer intento el lienzo sigue siendo **solo texto plano**, el segundo intento debe orientarse a: **subir imagen de fondo o logo** (jobs de asset/upload que exponga el toolkit), **duplicar y retocar** un diseno maestro ya bonito en la cuenta, o **handoff** con lista corta de 3 ajustes en el editor (color fondo, tamano titular, logo).

## Caption e hashtags

- **Caption:** 150–300 caracteres: linea gancho + valor + CTA; tono de `product-marketing-context`.
- **Hashtags:** mezcla alcance (amplios) + nicho (especificos del cliente); sin spam; respetar politica del cliente y plataforma.

## Pipeline end-to-end automatizado (comportamiento por defecto si hay herramientas)

**Objetivo:** que Jarvis / `mkt-*` hagan **todo el trabajo programable** en una sola peticion: guion + creacion en Canva + export (o URLs de descarga), **sin** pedir al humano que abra Canva salvo fallo de API.

**Precondiciones (config una vez en el host, no en cada post):** plugin Composio + OAuth Canva activo en Composio; `tools.alsoAllow` con las siete `COMPOSIO_*`; verificacion con `openclaw composio doctor` (lista de 7 herramientas + **healthy**). **Nota:** si tras el doctor aparece `MCP client connection failed: fetch failed`, eso **no** invalida solo la configuracion: el criterio real es que el **gateway** pueda invocar `COMPOSIO_*` en chat; ver [TROUBLESHOOTING_COMPOSIO_OPENCLAW.md](../../../../docs/TROUBLESHOOTING_COMPOSIO_OPENCLAW.md). Con herramientas respondiendo, en **runtime** no debe hacer falta intervencion humana para autenticar.

**Secuencia obligatoria** cuando el encargo incluye diseno IG y las herramientas estan en contexto:

1. `COMPOSIO_SEARCH_TOOLS` (o equivalente) para localizar acciones del toolkit Canva vigentes.
2. **Brief visual** (seccion anterior): si hay brand templates, **listar → dataset → autofill** primero; si no, preparar crear diseno con **fondo + assets** en el mismo razonamiento (no solo titular suelto).
3. Crear diseno y/o autofill segun disponibilidad (dimensiones 1080x1350 o la elegida).
4. Si el resultado es anti-patron (solo texto plano sin capas utiles), **segundo intento** con upload de fondo/logo o duplicar maqueta previa; si la API no lo permite, **handoff** con `edit_url` y checklist de 3 retoques.
5. Lanzar export y recuperar URL de descarga o estado del job.
6. Incluir en la respuesta: **IDs de diseno**, **URL de edicion** en Canva si la API la devuelve ([design edit handoff](https://www.canva.dev/docs/mcp/workflows/design-edit/)), y **enlace/credenciales del export**.
7. **No** cerrar el turno solo con markdown de "aqui tu copy" si el usuario pidio post con diseno y las herramientas respondieron OK.

Si las herramientas **no** estan disponibles o la API falla: declararlo en una frase y entregar brief + assets para recuperacion manual.

## Salida esperada del agente

Siempre entregar en markdown **al menos**:

1. **Titulo del carrusel** + ratio elegido (ej. 4:5).
2. **Lista numerada** de slides: titulo / bullets / nota visual (opcional).
3. **Caption** + bloque de hashtags sugeridos.

Si el pipeline Canva se ejecuto con exito, **anadir**:

4. **Evidencia de diseno:** `design_id`(s), enlaces **Editar en Canva** si aplican, URL(s) de export o estado del job.
5. **AG-03** solo si el siguiente paso es **publicar en Instagram** (no para el mero borrador/export).

## Herramientas de diseno (opcionales, fuera del repo)

### A. open-carrusel (local, export PNG)

Instalado en `~/tools/open-carrusel/` (no en el monorepo). Genera slides HTML y exporta PNGs a dimensiones exactas IG. El humano pega el guion de este skill, edita y exporta.

```bash
cd ~/tools/open-carrusel && npm run dev   # http://localhost:3000
```

### B. Canva via Composio (API remota — ya activa)

Plugin `composio` instalado en OpenClaw. Permite a Jarvis y `mkt-*` crear disenos, usar brand templates y exportar desde chat. Herramientas clave:

- `create_canva_design_with_optional_asset` — crear diseno.
- `initiate_canva_design_autofill_job` — autofill brand templates.
- `initiates_canva_design_export_job` — exportar a PNG/PDF.
- `list_user_designs` — listar disenos existentes.

Requiere `consumerKey` de Composio configurado en `~/.openclaw/openclaw.json`. Autenticar Canva desde [dashboard.composio.dev](https://dashboard.composio.dev).

### C. Canva Connect directo (skill `canva` — OAuth sin intermediario)

Skill [`canva`](../canva/SKILL.md) instalado desde ClawHub (`openclaw skills install canva`). Accede a la Connect API de Canva **directamente** via OAuth 2.0, sin pasar por Composio.

**Scripts:**

- `scripts/canva-auth.sh` — flujo OAuth interactivo (genera `~/.canva/tokens.json`).
- `scripts/canva.sh <comando>` — CLI: `designs`, `get <id>`, `templates`, `export <id> [png|jpg|pdf]`, `autofill <template_id> '<json>'`, `upload <archivo>`, `user`.

**Requisitos:**

- `CANVA_CLIENT_ID` y `CANVA_CLIENT_SECRET` como env vars (crearlos en [canva.dev/developers](https://www.canva.dev/docs/connect/)).
- Scopes: `design:content:read`, `design:content:write`, `asset:read`, `asset:write`, `brandtemplate:content:read`.

**Cuando usar uno u otro:**

| Criterio | Composio (B) | Canva Connect directo (C) |
|----------|-------------|--------------------------|
| Auth gestionada | Si (Composio OAuth) | Manual (script + tokens locales) |
| Intermediario | Si (MCP Composio) | No (API Canva directo) |
| Funciona en `messaging` profile | Si (via `COMPOSIO_*` en `alsoAllow`) | Si (via `exec` de scripts en sesion) |
| Autofill brand templates | Si | Si |
| Ideal para | Chat Telegram/Discord (tool calling) | CLI, scripts automatizados, debug |

### D. Canva MCP oficial (futuro — `generate-design` + editing)

Servidor remoto `https://mcp.canva.com/mcp` — 30+ herramientas incluyendo `generate-design` (IA), `perform-editing-operations` (editar texto en lienzo), `resize-design` (Pro+). Acceso: [Canva MCP Connector Intake Form](https://docs.google.com/forms/d/e/1FAIpQLSdtsKA9LSmY-JEf_nF5QYBdjxfnXbgqvlKzd8obKGSPSK_eOA/viewform) (OAuth Redirect URI obligatorio; el formulario lista capacidades y el snippet `mcp-remote`). Documentacion oficial: [Overview MCP](https://www.canva.dev/docs/mcp/), [herramientas y rate limits](https://www.canva.dev/docs/mcp/tools/), [design edit handoff](https://www.canva.dev/docs/mcp/workflows/design-edit/) (siempre ofrecer enlace de edicion en Canva), [troubleshooting](https://www.canva.dev/docs/mcp/troubleshooting/), [usage policy](https://www.canva.dev/docs/mcp/usage-policy/), [prohibited use](https://www.canva.dev/docs/mcp/prohibited-use/).

---

## Dimensiones por red social (referencia ampliada)

| Red | Formato | Pixeles | Ratio | Notas |
|-----|---------|---------|-------|-------|
| **Instagram** | Post feed cuadrado | 1080 x 1080 | 1:1 | |
| **Instagram** | Post feed retrato | 1080 x 1350 | 4:5 | Recomendado carrusel |
| **Instagram** | Story / Reels | 1080 x 1920 | 9:16 | |
| **Instagram** | Carrusel | 1080 x 1350 | 4:5 | Max 10 slides |
| **Facebook** | Post con imagen | 1200 x 630 | ~1.91:1 | |
| **Facebook** | Story | 1080 x 1920 | 9:16 | |
| **LinkedIn** | Post con imagen | 1200 x 627 | ~1.91:1 | |
| **LinkedIn** | Carrusel (PDF) | 1080 x 1080 o 1080x1350 | 1:1 o 4:5 | Subir como PDF |
| **X (Twitter)** | Post con imagen | 1600 x 900 | 16:9 | |
| **TikTok** | Video / imagen | 1080 x 1920 | 9:16 | |
| **Pinterest** | Pin estandar | 1000 x 1500 | 2:3 | |

---

## Flujo operativo Canva automatizado (patron social media)

Flujo tipo para **crear un post de Instagram** con la API (aplica a Composio, skill directo o MCP):

1. **Listar brand templates** — `GET /brand-templates` o via Composio. Si hay plantilla adecuada, usarla; si no, crear diseno en blanco.
2. **Autofill** (si hay brand template) — `POST /autofills` con `brand_template_id` + `data: {titulo, cuerpo, ...}`. Requiere campos definidos en la plantilla. **Nota:** brand templates suelen necesitar Canva Teams/Enterprise; cuenta gratis puede devolver `items: []`.
3. **Crear diseno** (si no hay template) — dimensiones custom (ej. 1080x1350 para IG carrusel).
4. **Subir asset** — `POST /asset-uploads` con imagen de producto, logo, foto.
5. **Exportar** — `POST /exports` con `design_id` + formato (PNG 1080x1350). Pollear status hasta `completed`.
6. **Descargar** — URL temporal del export; entregar al usuario. **AG-03** solo si va a **publicarse** en IG, no por el export en si.

**Para carrusel:** repetir pasos 2-5 por cada slide (max 10).

**Fallback si la API no esta disponible:** entregar brief textual por slide + URLs de assets para montaje manual en canva.com.

---

**Redactar no es crear en Canva:** entregar titular, cuerpo, guion por slide o URLs de imagenes **no** genera por si solo un **archivo** en la cuenta de Canva. Eso solo ocurre si se **ejecutan** las acciones de API (crear diseno / export) via Composio, el skill `canva` o el MCP oficial, o si el humano monta el lienzo a mano en canva.com.

**Si el humano pide explicitamente "crear el diseno en Canva" o "que quede en mi Canva":**

1. **Intentar** primero Composio (tool calling desde chat), luego skill `canva` (scripts CLI).
2. Si **no** hay herramientas disponibles, falla la auth, o la llamada devuelve error: **decirlo en una frase clara** ("No se creo ningun lienzo en Canva en esta sesion") y entonces dar el **brief** por slide + enlaces a assets para montaje manual.
3. **No** presentar solo texto bonito como si ya existiera un diseno guardado en Canva; distinguir siempre **borrador de contenido** vs **diseno creado en la plataforma**.

**Plantillas "del buscador" vs API:** las plantillas **predisenadas del explorador web** (Redes → Instagram → elegir miniatura) **no** son seleccionables por la Connect API como “usa la plantilla X del catalogo”. Composio puede **crear lienzo** (dimensiones) + **assets** + **export**; para **misma estructura que una plantilla concreta** hace falta **Brand template** del equipo (campos de datos + autofill, suele Enterprise) o flujo hibrido (humano clona una vez en Canva y el API trabaja sobre copias). Si el usuario espera **pixel-perfect** como el buscador: decirlo en una frase y remitir a [CAROUSEL_IG_JARVIS.md](../../../../docs/CAROUSEL_IG_JARVIS.md) seccion plantillas del explorador.

### Flujo combinado

1. Este skill genera el **guion** (slides, caption, hashtags).
2. **Por defecto** el ecosistema usa **Composio (B)** para Canva en el gateway; el agente no debe delegar en el humano "ve a Canva" si las herramientas estan disponibles.
3. **open-carrusel** (A) solo si no hay API o el humano exige control local.
4. **Canva Connect directo** (C) o **MCP oficial** (D) segun config futura.
5. **Publicar** en la red social: **AG-03** (aprobacion CEO). Crear/exportar borrador en Canva **no** cuenta como publicacion.

Ver [CAROUSEL_IG_JARVIS.md](../../../../docs/CAROUSEL_IG_JARVIS.md) para detalle completo.

## Limites

- No sustituye revision legal de claims (salud, finanzas, resultados garantizados).
- No **publicar** en redes sin cumplir **AG-03** y politica del cliente; la generacion automatica de diseno/export es distinta de la publicacion.
- No commitear assets binarios grandes al monorepo; entregables en rutas acordadas ([JARVIS_DOCUMENTS_ON_DISK.md](../../../../docs/JARVIS_DOCUMENTS_ON_DISK.md)).
