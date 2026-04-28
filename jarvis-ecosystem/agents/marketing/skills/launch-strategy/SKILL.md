---
name: launch-strategy
description: "Lanzamientos de producto/feature: mensajes, canales y timeline. EN: launch strategy, GTM"
metadata:
  version: "1.1.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.1.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Lanzamientos de producto/feature: mensajes, canales y timeline.

### Cuándo usarla (disparadores)

- **ES:** `lanzamiento`, `go-to-market`, `release`
- **EN:** `launch strategy`, `GTM`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

Workflow **ops** relacionado: [`strategic-briefing-ops`](../../../jarvis/skills/strategic-briefing-ops/SKILL.md) (nombre distinto en Jarvis).

## Frameworks / metodología

### Marco de trabajo (estrategia / ideas)

#### Variante rápida relacionada

[strategic-briefing-ops](../../../jarvis/skills/strategic-briefing-ops/SKILL.md) — nombre distinto; úsala para sesiones cortas en chat.


### Hooks al pipeline Jarvis

| Skill / doc | Rol |
|-------------|-----|
| [`brand-kit`](../../../../skills/brand-kit/SKILL.md) | Identidad `brand.json` del dossier |
| [`activity-log`](../../../../skills/global/activity-log/SKILL.md) | Traza de tareas/eventos |
| [`handoff`](../../../../skills/global/handoff/SKILL.md) | Pass entregables entre agentes |


## Puertas de aprobación

- **AG-12**: publicar en canales externos o piezas listas para difusión masiva → aprobación previa.

## Coordinación (comandos reales)

Ejecutar desde la raíz del repo `jarvis-ecosystem/` (ajusta rutas si tu cwd es otro).

**1) Iniciar tarea**

```bash
bash skills/global/activity-log/bin/activity-log start \
  --agent mkt-strategy \
  --title "Brief / entrega skill" \
  --dossier <DOSSIER_ID> \
  --ref strategy
```

**2) Registrar hito / artefacto**

```bash
bash skills/global/activity-log/bin/activity-log event \
  --task <TASK_ID> \
  --agent mkt-strategy \
  --kind milestone \
  --note "Descripción breve del entregable"
```

**3) Handoff al siguiente rol**

```bash
bash skills/global/handoff/bin/handoff create \
  --from mkt-strategy \
  --to mkt-content \
  --schema research-to-strategy \
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
- [`paid-ads`](../paid-ads/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
