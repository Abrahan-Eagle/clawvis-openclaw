# Escalación asíncrona al CEO (Telegram, WhatsApp, etc.)

**Cuándo:** el agente necesita **decisión humana** pero el CEO **no está en chat síncrono**. El trabajo **no se pierde**: se empaqueta, se notifica por canal de mensajería y la tarea entra en estado **waiting_for_user**.

**Prerrequisitos:** canales ya configurados en OpenClaw ([`INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md`](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md)); bindings `agents.list[]` + `bindings` en `~/.openclaw/openclaw.json`.

---

## Triggers por modo (resumen)

| Modo | Escalar típicamente cuando… |
|------|-------------------------------|
| **D** | Cualquier AG de la tabla — comportamiento clásico (Trello + mensaje). |
| **C** | Salida al mundo exterior: AG-03, AG-04, AG-12, AG-13 (publicación/entrega); también AG-01, AG-02, AG-05, AG-06, AG-08, AG-09, AG-11 según impacto. |
| **B** | Como C; AG ampliados solo dentro de dossier aprobado — si hay duda, escalar. |
| **A** | Fuera de **ventana horaria** o fuera de **lista blanca** (cuenta/ruta/canal) → escalar como C. |

**Siempre CEO (no “auto-aprobación” por modo):** AG-05 (pagos), AG-07 (`openclaw.json`), AG-10 (destructivo), y revisión explícita de entrega/publicación con IA (**AG-13**).

---

## Payload recomendado

Campos mínimos (texto o JSON en el mensaje):

```json
{
  "escalation_id": "esc-YYYYMMDD-shortid",
  "gate": "AG-12",
  "agent_id": "mkt-social",
  "autonomy_mode": "C",
  "dossier_id": "cli-…",
  "summary": "Qué se propone y por qué",
  "risk_notes": "Legal / marca / datos personales",
  "artifacts": ["ruta/preview.png", "…"],
  "options": ["approve", "reject", "defer"],
  "deadline_suggested": "ISO8601 opcional"
}
```

---

## Opciones de respuesta del CEO

| Opción | Efecto |
|--------|--------|
| **approve** | El agente ejecuta la acción gateada y documenta en activity-log + Trello si aplica. |
| **reject** | Cancela; documentar razón en memoria / tarjeta. |
| **defer** | No ejecutar ahora; mantener tarea abierta o mover a backlog en Trello. |

---

## Estado en disco (`state/`)

Convención (compatible con [`activity-log`](../skills/global/activity-log/SKILL.md)):

1. **Tarea activa** ya tiene `task_id` de `activity-log start`.
2. Añadir evento `kind: escalation` con `note` que incluya `escalation_id` y canal usado.
3. Opcional: archivo `state/tasks/<task_id>.json` con campo `"status": "waiting_for_user"` y `"escalation": { ... }` hasta recibir respuesta.
4. Al responder el CEO: evento `kind: milestone` o cierre; **no** duplicar gates.

Los directorios `state/tasks/`, `state/handoffs/` pueden estar en `.gitignore` para runtime local; la **convención** vale aunque el fichero no se suba a Git.

---

## Integración OpenClaw / mensajería

- El gateway ya puede enlazar **Telegram**, **WhatsApp**, **Discord**, etc. La escalación es **mensaje humano** al CEO con el payload en el cuerpo.
- No asumir que el bot “entiende” botones nativos en todos los canales: texto plano con prefijo `approve AG-12 esc-…` es suficiente.
- **Coste:** si el modelo debe cotizar el turno, ver [`economic-accountability-ops`](../skills/global/economic-accountability-ops/SKILL.md).

---

## Auditoría previa (opcional)

Antes de escalar, el agente puede ejecutar [`llm-as-judge-ops`](../agents/jarvis/skills/llm-as-judge-ops/SKILL.md). Si `must_fix` no está vacío, **corregir antes** de molestar al CEO salvo urgencia.

---

## Historial

- **2026-04-28:** Versión inicial alineada con modos A/B/C/D y [AUTONOMIA_MODOS.md](AUTONOMIA_MODOS.md).
