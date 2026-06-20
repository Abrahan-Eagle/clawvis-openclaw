---
name: task-pipeline-ops
description: >
  Pipeline multi-paso proyecto activo: Plan → Spec → Exec → Verify → Fix (máx. 3).
  Trigger: Pantallas complejas, varios providers, flujos multi-paso.
license: UNLICENSED
metadata:
  version: "1.1.0"
  auto_invoke:
    - "Iniciar módulo"
  related-skills: [jarvis-core, verification-before-completion, writing-plans]
---

# Task pipeline ops — proyecto activo

Adaptado desde clawvis-openclaw.

## Pipeline

```
PLAN → SPEC → EXEC → VERIFY → FIX (≤3) → COMPLETE | ESCALATE
```

## Fase PLAN

- `.agents/plans/implementation_plan.md`
- Aprobación usuario

## Fase SPEC

| Paso | Done when |
|------|-----------|
| Pantalla | Widget monta sin overflow; analyze limpio |
| Provider | Estado coherente; tests si existen |

## Fase VERIFY

- `flutter analyze` + `flutter test` (evidencia en el turno)

## Cierre

- `walkthrough.md` + opcional `docs/active_context.md` vía `session-learner-ops`

---

## Overlay clawvis — holding OpenClaw

### Alcance

Secuencia plan → spec → exec → verify → fix para tareas del **holding** (scripts, ClawFlows, integraciones OpenClaw).

### Gates

- Acciones con impacto externo: [APPROVAL_GATES.md](../../../docs/APPROVAL_GATES.md)
- Trello: tarjeta formal según [FLUJO_TRELLO_ECOSISTEMA.md](../../../docs/FLUJO_TRELLO_ECOSISTEMA.md)

### Verificación

Cerrar con `verification-before-completion`; commits con `structured-commits-ops` si hay decisión de arquitectura.
