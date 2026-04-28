---
name: video
description: "Guiones y pipeline de video corto con tts/subtitles/video-compose del ecosistema. EN: short video, reel"
metadata:
  version: "1.0.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.0.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Guiones y pipeline de video corto con tts/subtitles/video-compose del ecosistema.

### Cuándo usarla (disparadores)

- **ES:** `reel`, `video corto`, `subtítulos`
- **EN:** `short video`, `reel`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

No hay `*-ops` homónima en Jarvis para esta skill; usa la skill completa y skills globales (`brand-kit`, `carousel-render`, …).

## Frameworks / metodología

### Enfoques de video (ecosistema Jarvis)

| Enfoque | Skill local |
|---------|---------------|
| Voz + subs + montaje | [`tts-free`](../../../../skills/tts-free/SKILL.md) → [`subtitles`](../../../../skills/subtitles/SKILL.md) → [`video-compose`](../../../../skills/video-compose/SKILL.md) |
| Plantilla animada | [`video-short`](../../../../skills/video-short/SKILL.md) |

#### Workflow reel corto (vertical)

1. Frames 9:16 con `image-render` si aplica.
2. `tts-free synthesize --with-subs`
3. `subtitles` (SRT/ASS) al estilo marca.
4. `video-compose render` → MP4 en `out/`.

Doc: [`docs/REELS_TIKTOK_PIPELINE_FREE.md`](../../../../docs/REELS_TIKTOK_PIPELINE_FREE.md).


### Hooks al pipeline Jarvis

| Hook |
|------|
| `tts-free` → `subtitles` → `video-compose`; opcional `video-short`. |


## Puertas de aprobación

- **AG-13**: IA generativa en assets que se entreguen o publiquen → [`docs/APPROVAL_GATES.md`](../../../../docs/APPROVAL_GATES.md).

## Coordinación (comandos reales)

Ejecutar desde la raíz del repo `jarvis-ecosystem/` (ajusta rutas si tu cwd es otro).

**1) Iniciar tarea**

```bash
bash skills/global/activity-log/bin/activity-log start \
  --agent mkt-social \
  --title "Brief / entrega skill" \
  --dossier <DOSSIER_ID> \
  --ref creative-pipeline
```

**2) Registrar hito / artefacto**

```bash
bash skills/global/activity-log/bin/activity-log event \
  --task <TASK_ID> \
  --agent mkt-social \
  --kind milestone \
  --note "Descripción breve del entregable"
```

**3) Handoff al siguiente rol**

```bash
bash skills/global/handoff/bin/handoff create \
  --from mkt-social \
  --to design \
  --schema design-to-producer \
  --task <TASK_ID> \
  --payload-file /tmp/handoff-payload.json
```

**4) Cerrar**

```bash
bash skills/global/activity-log/bin/activity-log end \
  --task <TASK_ID> \
  --note "Listo para revisión CEO/cliente"
```

Lista de schemas: `bash skills/global/handoff/bin/handoff schemas`.


### Skills relacionadas (mapa local)

- [`social-content`](../social-content/SKILL.md)
- [`copywriting`](../copywriting/SKILL.md)
- [`image`](../image/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
