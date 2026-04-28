---
name: social-content
description: "Estrategia y piezas para redes (hooks, calendario, repurposing) enlazando pipeline jarvis. EN: social content, LinkedIn, content calendar"
metadata:
  version: "1.3.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.3.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Estrategia y piezas para redes (hooks, calendario, repurposing) enlazando pipeline jarvis.

### Cuándo usarla (disparadores)

- **ES:** `Instagram`, `LinkedIn`, `calendario editorial`, `short-form`
- **EN:** `social content`, `LinkedIn`, `content calendar`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

No hay `*-ops` homónima en Jarvis para esta skill; usa la skill completa y skills globales (`brand-kit`, `carousel-render`, …).

## Frameworks / metodología

### Marco de trabajo (contenido social)

#### Pipeline RRSS gratis (Jarvis)

1. [`brand-kit`](../../../../skills/brand-kit/SKILL.md) — validar `brand.json` del dossier.
2. Copy / guion — esta skill + [`copywriting`](../copywriting/SKILL.md).
3. Carruseles estáticos: [`carousel-render`](../../../../skills/carousel-render/SKILL.md); IA opcional: [`image-ai-free`](../../../../skills/image-ai-free/SKILL.md) (**AG-13**).
4. Variante corta de slides: [`carousel-ops`](../../../jarvis/skills/carousel-ops/SKILL.md).

Documentación: [`docs/CAROUSEL_PIPELINE_FREE.md`](../../../../docs/CAROUSEL_PIPELINE_FREE.md), [`docs/REELS_TIKTOK_PIPELINE_FREE.md`](../../../../docs/REELS_TIKTOK_PIPELINE_FREE.md).


### Hooks al pipeline Jarvis

| Hook |
|------|
| `brand-kit` — validar identidad del dossier. |
| `carousel-render` / `carousel-ops` — carruseles. |
| `docs/CAROUSEL_PIPELINE_FREE.md`, `docs/REELS_TIKTOK_PIPELINE_FREE.md`. |


## Puertas de aprobación

- **AG-13**: IA generativa en assets que se entreguen o publiquen → [`docs/APPROVAL_GATES.md`](../../../../docs/APPROVAL_GATES.md).
- **AG-12**: publicar en canales externos o piezas listas para difusión masiva → aprobación previa.

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

- [`copywriting`](../copywriting/SKILL.md)
- [`image`](../image/SKILL.md)
- [`video`](../video/SKILL.md)
- [`page-cro`](../page-cro/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
