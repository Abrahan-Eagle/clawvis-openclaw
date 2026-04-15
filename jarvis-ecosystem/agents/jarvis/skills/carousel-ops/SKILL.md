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

## Herramienta opcional (fuera del repo)

Quien necesite **export PNG** con preview y zip local puede instalar [open-carrusel](https://github.com/Hainrixz/open-carrusel) en su maquina; no es requisito del ecosistema. Ver [CAROUSEL_IG_JARVIS.md](../../../../docs/CAROUSEL_IG_JARVIS.md).

## Limites

- No sustituye revision legal de claims (salud, finanzas, resultados garantizados).
- No publicar sin cumplir **AG-03** y politica del cliente en redes.
- No commitear assets binarios grandes al monorepo; entregables en rutas acordadas ([JARVIS_DOCUMENTS_ON_DISK.md](../../../../docs/JARVIS_DOCUMENTS_ON_DISK.md)).
