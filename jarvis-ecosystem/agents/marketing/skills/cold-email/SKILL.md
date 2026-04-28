---
name: cold-email
description: "Cold email B2B y secuencias cortas orientadas a respuesta. EN: cold email, outreach"
metadata:
  version: "1.1.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.1.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Cold email B2B y secuencias cortas orientadas a respuesta.

### Cuándo usarla (disparadores)

- **ES:** `cold email`, `prospección`, `outreach`
- **EN:** `cold email`, `outreach`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

Variante corta **ops**: [`cold-email-ops`](../../../jarvis/skills/cold-email-ops/SKILL.md). Usa **esta skill completa** con dossier/brief formal.

## Frameworks / metodología

### Marco de trabajo (cold email)

#### Reglas

- Corto (<150 palabras primer touch); personalización demostrable; un CTA.
- Sin adjuntos en primer email salvo que el prospect lo pida.

#### Variante rápida

[cold-email-ops](../../../jarvis/skills/cold-email-ops/SKILL.md).


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
  --ref copy
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
  --schema copy-to-design \
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
- [`sales-enablement`](../sales-enablement/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
