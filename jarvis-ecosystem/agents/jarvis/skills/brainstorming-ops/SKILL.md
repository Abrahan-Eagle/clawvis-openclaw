---
name: brainstorming-ops
description: >
  OBLIGATORIO antes de tareas complejas en proyecto activo: pantallas, providers, navegación,
  flujos KYC/onboarding. Propone alternativas y obtiene aprobación antes de codificar.
  Trigger: Planificar módulo, feature ambiguo, rediseño UI.
license: UNLICENSED
metadata:
  author: proyecto Team
  version: "1.0.0"
  scope: [root]
  auto_invoke:
    - "Planificar desarrollo"
    - "Iniciar módulo"
  related-skills:
    - deep-interview-ops
    - jarvis-core
    - product-ui-design
---

# Brainstorming ops — proyecto activo

Adaptado desde clawvis-openclaw.

## Regla

**NO escribir código** hasta diseño aprobado por el usuario.

## Cuándo se activa

- Nueva pantalla o flujo (marketplace, chat, perfil, KYC)
- Cambios en Provider / navegación
- Tema, accesibilidad, responsive
- Integración API nueva en servicios

## Checklist

1. Leer `AGENTS.md`, `docs/active_context.md`, `{producto}-flutter-arch`, `{producto}-ui-design`.
2. Preguntas clarificadoras.
3. 2–3 alternativas (widgets, estado, rutas).
4. Plan en `.agents/plans/implementation_plan.md`.
5. OK del usuario.

## Secuencia

```
deep-interview-ops (si vago) → brainstorming-ops → task-pipeline-ops → ejecución
```

## Contexto proyecto

- Siempre `AppConfig.apiUrl` — sin URLs hardcodeadas.
- Provider + servicios por feature.
- Tema: `corral_x_theme.dart`.

---

## Overlay clawvis — holding OpenClaw

NO ejecutar ninguna acción hasta presentar un diseño y obtener aprobación del **CEO** o del agente coordinador.

### Cuándo se activa (holding)

- Propuesta comercial a un cliente
- Campaña de marketing nueva
- Nuevo script o automatización (`scripts/`, ClawFlows)
- Cambio en `openclaw.json` o integraciones
- Cualquier tarea que toque más de un agente o empresa del holding

### Checklist holding

1. Explorar contexto — dossier (`client-dossiers/`), Trello, MEMORY.md
2. Preguntas clarificadoras — una a la vez
3. Proponer 2–3 alternativas con trade-offs
4. Presentar diseño; documentar en tarjeta Trello o `memory/`
5. Aprobación CEO si aplica Approval Gate — [APPROVAL_GATES.md](../../../docs/APPROVAL_GATES.md)

### Proceso por tipo

- **Propuesta comercial:** dossier → borrador → AG-01 → enviar
- **Campaña marketing:** goals G-M* → plan → AG-03 → ejecutar
- **Script/automatización:** revisar CLAWFLOWS.md → diseño → `verification-before-completion`
