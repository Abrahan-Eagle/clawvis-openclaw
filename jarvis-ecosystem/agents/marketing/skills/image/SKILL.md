---
name: image
description: "Briefs y producción de imágenes de marketing enlazando render local e IA gratuita. EN: marketing image, thumbnail"
metadata:
  version: "1.0.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.0.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Briefs y producción de imágenes de marketing enlazando render local e IA gratuita.

### Cuándo usarla (disparadores)

- **ES:** `hero image`, `thumbnail`, `creatividades estáticas`
- **EN:** `marketing image`, `thumbnail`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

No hay `*-ops` homónima en Jarvis para esta skill; usa la skill completa y skills globales (`brand-kit`, `carousel-render`, …).

## Frameworks / metodología

### Enfoques de producción (ecosistema Jarvis)

| Enfoque | Cuándo | Skill local |
|---------|--------|-------------|
| Render determinista | Carruseles OG, layouts | [`image-render`](../../../../skills/image-render/SKILL.md) |
| IA gratuita (online) | Variaciones creativas sin presupuesto | [`image-ai-free`](../../../../skills/image-ai-free/SKILL.md) — **AG-13** |
| Carrusel multi-slide | Varias slides coherentes | [`carousel-render`](../../../../skills/carousel-render/SKILL.md) |
| Identidad | Tipografía/color | [`brand-kit`](../../../../skills/brand-kit/SKILL.md) |

#### Workflow ejemplo (carrusel + marca)

1. `brand-kit validate --dossier <id>`
2. `carousel-render` / `image-render` según docs RRSS.
3. Registrar artefacto con `activity-log`.

#### Nota sobre upstream

El texto upstream puede mencionar herramientas comerciales (Midjourney, APIs de pago). En este holding **prioriza** el stack local/documentado salvo aprobación explícita (**AG-13** / presupuesto).


### Hooks al pipeline Jarvis

| Hook |
|------|
| `image-render`, `image-ai-free`, `carousel-render`, `brand-kit` (Tabla en marco de trabajo). |


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
- [`page-cro`](../page-cro/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
