---
name: lead-magnets
description: "Diseña lead magnets para captura y nutrición. EN: lead magnet, downloadable"
metadata:
  version: "1.0.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.0.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Diseña lead magnets para captura y nutrición.

### Cuándo usarla (disparadores)

- **ES:** `lead magnet`, `descargable`, `checklist`
- **EN:** `lead magnet`, `downloadable`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

No hay `*-ops` homónima en Jarvis para esta skill; usa la skill completa y skills globales (`brand-kit`, `carousel-render`, …).

## Frameworks / metodología

### Marco de trabajo (growth engineering)

#### Principios

- Hipótesis → MVP barato → medición.
- Herramientas gratuitas / contenido evergreen cuando el presupuesto es cero.


### Hooks al pipeline Jarvis

| Skill / doc | Rol |
|-------------|-----|
| [`brand-kit`](../../../../skills/brand-kit/SKILL.md) | Identidad `brand.json` del dossier |
| [`activity-log`](../../../../skills/global/activity-log/SKILL.md) | Traza de tareas/eventos |
| [`handoff`](../../../../skills/global/handoff/SKILL.md) | Pass entregables entre agentes |


## Puertas de aprobación

- Sin gates extra por defecto; ante reputación/pagos/datos sensibles revisa [`docs/APPROVAL_GATES.md`](../../../../docs/APPROVAL_GATES.md).

## Coordinación (comandos reales)

Ejecutar desde la raíz del repo `jarvis-ecosystem/` (ajusta rutas si tu cwd es otro).

**1) Iniciar tarea**

```bash
bash skills/global/activity-log/bin/activity-log start \
  --agent mkt-growth \
  --title "Brief / entrega skill" \
  --dossier <DOSSIER_ID> \
  --ref growth
```

**2) Registrar hito / artefacto**

```bash
bash skills/global/activity-log/bin/activity-log event \
  --task <TASK_ID> \
  --agent mkt-growth \
  --kind milestone \
  --note "Descripción breve del entregable"
```

**3) Handoff al siguiente rol**

```bash
bash skills/global/handoff/bin/handoff create \
  --from mkt-growth \
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

- [`email-sequence`](../email-sequence/SKILL.md)
- [`page-cro`](../page-cro/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
