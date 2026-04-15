# Carruseles Instagram en el ecosistema Jarvis

## Que queda en el repo (lo necesario)

- **Skill [`carousel-ops`](../agents/jarvis/skills/carousel-ops/SKILL.md):** guion por slides, dimensiones IG, reglas de diseno legibles, caption/hashtags, cumplimiento **AG-03**.
- Referencia en [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) §2.9.

Con eso Jarvis y `mkt-*` pueden **planificar y redactar** carruseles sin instalar nada mas.

## Lo que se desecha para este monorepo

- **App open-carrusel completa** (Next.js 16, Puppeteer ~300 MB Chromium, servidor local :3000).
- **Dependencia del Claude CLI** embebido en esa app para el chat in-app.
- **Submodulo, fork dentro de `clawvis-openclaw`** o job de CI que levante esa stack.

Motivo: peso, mantenimiento y desacople del gateway OpenClaw; el valor para el holding esta en **criterios y proceso**, no en otro `node_modules` gigante.

## Opcional para quien disena en PC

El upstream [Hainrixz/open-carrusel](https://github.com/Hainrixz/open-carrusel) (MIT) genera slides HTML y exporta PNGs a medida IG. Si un operador lo instala **fuera** del repo (`git clone` en su home o `~/tools/`), puede usar el mismo briefing que preparo el skill `carousel-ops`. Eso es decision local del humano, no del bot.

## Resumen

| Pregunta | Respuesta |
|----------|-----------|
| ¿Jarvis necesita open-carrusel instalado? | **No.** |
| ¿Que necesita el ecosistema? | Skill + gobierno (dossier, Trello, AG-03). |
| ¿Donde estan los PNG? | Donde el humano los exporte (app opcional o Canva/Figma). |
