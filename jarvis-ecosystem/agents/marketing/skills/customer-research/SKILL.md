---
name: customer-research
description: "Investigación de clientes: entrevistas, VOC y JTBD con enlace a ops corta. EN: customer research, JTBD"
metadata:
  version: "1.0.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.0.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Investigación de clientes: entrevistas, VOC y JTBD con enlace a ops corta.

### Cuándo usarla (disparadores)

- **ES:** `entrevistas`, `JTBD`, `insights clientes`
- **EN:** `customer research`, `JTBD`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

Variante corta **ops**: [`deep-interview-ops`](../../../jarvis/skills/deep-interview-ops/SKILL.md). Usa **esta skill completa** con dossier/brief formal.

## Frameworks / metodología

### Marco de trabajo (investigación de clientes)

#### Modos

1. **Activos existentes**: entrevistas, tickets, encuestas → VOC.
2. **Desk research**: fuentes públicas; automatización web puede requerir **AG-11**.

#### Variante rápida

[deep-interview-ops](../../../jarvis/skills/deep-interview-ops/SKILL.md).


### Hooks al pipeline Jarvis

| Skill / doc | Rol |
|-------------|-----|
| [`brand-kit`](../../../../skills/brand-kit/SKILL.md) | Identidad `brand.json` del dossier |
| [`activity-log`](../../../../skills/global/activity-log/SKILL.md) | Traza de tareas/eventos |
| [`handoff`](../../../../skills/global/handoff/SKILL.md) | Pass entregables entre agentes |


## Puertas de aprobación

- **AG-11**: automatizar dominio nuevo en Playwright / scraping → aprobación antes de `BROWSER_PLAYWRIGHT_ALLOW`.

## Coordinación (comandos reales)

Ejecutar desde la raíz del repo `jarvis-ecosystem/` (ajusta rutas si tu cwd es otro).

**1) Iniciar tarea**

```bash
bash skills/global/activity-log/bin/activity-log start \
  --agent mkt-research \
  --title "Brief / entrega skill" \
  --dossier <DOSSIER_ID> \
  --ref customer-research
```

**2) Registrar hito / artefacto**

```bash
bash skills/global/activity-log/bin/activity-log event \
  --task <TASK_ID> \
  --agent mkt-research \
  --kind milestone \
  --note "Descripción breve del entregable"
```

**3) Handoff al siguiente rol**

```bash
bash skills/global/handoff/bin/handoff create \
  --from mkt-research \
  --to mkt-strategy \
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

- [`product-marketing-context`](../product-marketing-context/SKILL.md)
- [`copywriting`](../copywriting/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
