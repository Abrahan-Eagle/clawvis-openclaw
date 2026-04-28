---
name: page-cro
description: "Diagnóstico y mejoras de conversión en páginas de marketing. EN: landing page, conversion rate, CRO"
metadata:
  version: "1.1.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.1.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Diagnóstico y mejoras de conversión en páginas de marketing.

### Cuándo usarla (disparadores)

- **ES:** `optimizar landing`, `subir conversión`, `hero`, `CTA`
- **EN:** `landing page`, `conversion rate`, `CRO`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

Variante corta **ops**: [`page-cro-ops`](../../../jarvis/skills/page-cro-ops/SKILL.md). Usa **esta skill completa** con dossier/brief formal.

## Frameworks / metodología

### Marco de trabajo (CRO de página)

**Objetivo:** subir conversión en páginas clave (landing, pricing, features).

#### Principios (adaptación Jarvis)

- Claridad del mensaje en <5 s (hero).
- Propuesta de valor específica vs genérica.
- Prueba social creíble cerca del CTA.
- Una acción primaria por vista; repetir CTA en puntos de decisión.
- Fricción mínima: campos necesarios, rendimiento, sin distracciones que compitan con la meta.

#### Variante rápida (`*-ops`)

Para iteración corta en chat sin brief formal: [page-cro-ops](../../../jarvis/skills/page-cro-ops/SKILL.md).

#### Contexto de cliente

Parte siempre de `client-dossiers/<dossier_id>/marketing-context.md` (ICP, objeciones, lenguaje del cliente).


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
  --agent mkt-content \
  --title "Brief / entrega skill" \
  --dossier <DOSSIER_ID> \
  --ref cro
```

**2) Registrar hito / artefacto**

```bash
bash skills/global/activity-log/bin/activity-log event \
  --task <TASK_ID> \
  --agent mkt-content \
  --kind milestone \
  --note "Descripción breve del entregable"
```

**3) Handoff al siguiente rol**

```bash
bash skills/global/handoff/bin/handoff create \
  --from mkt-content \
  --to mkt-social \
  --schema strategy-to-copy \
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
- [`analytics-tracking`](../analytics-tracking/SKILL.md)
- [`ab-test-setup`](../ab-test-setup/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
