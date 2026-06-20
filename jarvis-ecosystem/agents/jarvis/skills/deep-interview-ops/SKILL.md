---
name: deep-interview-ops
description: >
  Entrevista socrática antes de tareas ambiguas en proyecto activo. Gate claridad mínima 3.5/5.
  Trigger: UI vaga, flujo KYC/onboarding sin spec, cambios navegación global.
license: UNLICENSED
metadata:
  version: "1.1.0"
  auto_invoke:
    - "Requisitos ambiguos"
  related-skills:
    - brainstorming-ops
    - product-kyc-ui
---

# Deep interview ops — proyecto activo

> Con Spec Kit (`.specify/`), preferir `speckit-clarify` para clarificación estructurada de `spec.md`.

Adaptado desde clawvis-openclaw.

## Gate

```
NO EJECUTAR SI CLARIDAD PROMEDIO < 3.5 / 5.0
```

## Secuencia

`deep-interview-ops` → `brainstorming-ops` → ejecución

## 6 dimensiones

| Dimensión | Pregunta guía |
|-----------|---------------|
| Alcance | ¿Qué pantallas/widgets? ¿Web + móvil? |
| Criterio de éxito | ¿Analyze + tests + criterio UX? |
| Restricciones | ¿Tema claro/oscuro? ¿Offline? |
| Dependencias | ¿API lista en backend `dev`? |
| Riesgos | ¿BuildContext async? ¿Permisos cámara? |
| Contexto | ¿Stitch assets? ¿Walkthrough previo? |

## Casos típicos proyecto

- Onboarding + KYC UI
- Chat legibilidad / realtime
- Marketplace filtros y cards
- Mi Perfil / documentos rancho

---

## Overlay clawvis — holding OpenClaw

### Ventas / holding

- Activar frameworks **SPIN**, Gap Selling, **Sandler** para objeciones comerciales
- Gate claridad >= 3.5/5 antes de `proposal-ops` o envío Workana
- Leer `client-dossiers/` y contexto Trello del deal

### Referencias

[FLUJO_VENTAS_PROSPECCION_CIERRE.md](../../../docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md), [APPROVAL_GATES.md](../../../docs/APPROVAL_GATES.md).
