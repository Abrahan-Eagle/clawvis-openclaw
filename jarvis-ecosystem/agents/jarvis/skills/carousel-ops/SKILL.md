---
name: carousel-ops
description: "Carruseles Instagram: narrativa por slides, dimensiones IG, tipografia y contraste, caption/hashtags, citas de marca — sin depender de apps externas en el repo. Opcional: herramienta local open-carrusel solo si el operador la instala aparte."
---

# Carousel ops (Instagram)

**Qué se toma del proyecto [open-carrusel](https://github.com/Hainrixz/open-carrusel) (MIT):** criterios de diseno, arco narrativo por slides, reglas de HTML seguro, dimensiones IG, caption/hashtags. **Qué se descarta para el ecosistema:** la app Next.js, Puppeteer, Chromium y el chat acoplado a Claude CLI **no** forman parte del repo ni del gateway OpenClaw.

Este skill cubre **metodologia y salidas textuales** (guion por slide, checklist, caption). La produccion de PNG pixel-perfect es **opcional** y solo si un humano instala open-carrusel fuera del monorepo — ver [CAROUSEL_IG_JARVIS.md](../../../../docs/CAROUSEL_IG_JARVIS.md).

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
| **Solo copy o tambien diseno?** (Canva / open-carrusel / texto con URLs de imagen) | Evita prometer “diseño en Canva” si el humano solo pidio articulo de blog. |
| **Marca y ratio?** (ej. IG 4:5, LinkedIn 1200x627) | Dimensiones y safe zone. |
| **Idioma y CTA?** | Coherencia con campana. |

Si el humano dice **“para IG”** o **“carrusel 6 slides”**, es suficiente; no hace falta repreguntar lo obvio.

## Prerrequisitos

1. Leer [`product-marketing-context.md`](../../../../.agents/product-marketing-context.md) (audiencia, voz, colores si estan declarados).
2. Si hay cliente: dossier en `client-dossiers/` y lineas rojas del encargo.
3. **Publicar** en IG: gate **AG-03** en [APPROVAL_GATES.md](../../../../docs/APPROVAL_GATES.md) — borrador + aprobacion CEO antes de publicar.

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

## Caption e hashtags

- **Caption:** 150–300 caracteres: linea gancho + valor + CTA; tono de `product-marketing-context`.
- **Hashtags:** mezcla alcance (amplios) + nicho (especificos del cliente); sin spam; respetar politica del cliente y plataforma.

## Salida esperada del agente

Entregar en markdown:

1. **Titulo del carrusel** + ratio elegido (ej. 4:5).
2. **Lista numerada** de slides: titulo / bullets / nota visual (opcional).
3. **Caption** + bloque de hashtags sugeridos.
4. **Checklist AG-03** si va a publicacion: pendiente aprobacion CEO.

No generar ni subir imagenes automaticamente desde el gateway.

## Herramientas de diseno (opcionales, fuera del repo)

### A. open-carrusel (local, export PNG)

Instalado en `~/tools/open-carrusel/` (no en el monorepo). Genera slides HTML y exporta PNGs a dimensiones exactas IG. El humano pega el guion de este skill, edita y exporta.

```bash
cd ~/tools/open-carrusel && npm run dev   # http://localhost:3000
```

### B. Canva via Composio (API remota)

Plugin `composio` instalado en OpenClaw. Permite a Jarvis y `mkt-*` crear disenos, usar brand templates y exportar desde chat. Herramientas clave:

- `create_canva_design_with_optional_asset` — crear diseno.
- `initiate_canva_design_autofill_job` — autofill brand templates.
- `initiates_canva_design_export_job` — exportar a PNG/PDF.
- `list_user_designs` — listar disenos existentes.

Requiere `consumerKey` de Composio configurado en `~/.openclaw/openclaw.json`. Autenticar Canva desde [dashboard.composio.dev](https://dashboard.composio.dev).

**Redactar no es crear en Canva:** entregar titular, cuerpo, guion por slide o URLs de imagenes **no** genera por si solo un **archivo** en la cuenta de Canva. Eso solo ocurre si se **ejecutan** las acciones de API (crear diseno / export) via Composio, o si el humano monta el lienzo a mano en canva.com.

**Si el humano pide explícitamente "crear el diseno en Canva" o "que quede en mi Canva":**

1. **Intentar** las herramientas Composio expuestas en la sesion (p. ej. buscar/ejecutar acciones del toolkit Canva: listar disenos, crear diseno, iniciar export) cuando el gateway las inyecte al modelo.
2. Si **no** hay herramientas disponibles, falla la auth, o la llamada devuelve error: **decirlo en una frase clara** ("No se creo ningun lienzo en Canva en esta sesion") y entonces si el **brief** por slide + enlaces a assets para montaje manual.
3. **No** presentar solo texto bonito como si ya existiera un diseno guardado en Canva; distinguir siempre **borrador de contenido** vs **diseno creado en la plataforma**.

### Flujo combinado

1. Este skill genera el **guion** (slides, caption, hashtags).
2. El operador elige: **open-carrusel** (control local) o **Canva/Composio** (templates de marca, API).
3. Resultado visual pasa por **AG-03** antes de publicar.

Ver [CAROUSEL_IG_JARVIS.md](../../../../docs/CAROUSEL_IG_JARVIS.md) para detalle completo de ambas herramientas.

## Limites

- No sustituye revision legal de claims (salud, finanzas, resultados garantizados).
- No publicar sin cumplir **AG-03** y politica del cliente en redes.
- No commitear assets binarios grandes al monorepo; entregables en rutas acordadas ([JARVIS_DOCUMENTS_ON_DISK.md](../../../../docs/JARVIS_DOCUMENTS_ON_DISK.md)).
