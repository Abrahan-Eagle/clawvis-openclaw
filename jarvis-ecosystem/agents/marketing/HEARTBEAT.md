# Heartbeat — Marketing (`mkt-*`)

Goal: G-M01 (presencia digital activa) + G-M02 (contenido alineado con ventas).
Modo autonomía recomendado: **C** (produce solo; publica solo con AG-12/13 CEO).

Todos los agentes `mkt-*` comparten este workspace. En cada pulso, identifica tu `agentId` de sesión y ejecuta **solo** el checklist de tu rol.

## Checklist común (todos los `mkt-*`)

1. `handoff list --open --to <MI_AGENT_ID>` — si hay handoffs abiertos >2h: `accept` o `reject` con razón.
2. `coordinator next --agent <MI_AGENT_ID>` (si el bin existe) — una unidad de trabajo pendiente.
3. Si el trabajo produce asset listo para publicar: **NO publiques**.
   - `judge-run --handoff <id> --category carousel_ig` (u otra categoría) → guardar path `state/judge/`
   - `activity-log block --reason "AG-12 pending"`
   - `approval-gate request --handoff <id> --ag AG-12 --task <task>`
   - Responde con el ID de escalación + judge file y **STOP**.
4. Fin de unidad / pre-handoff: aplicar [`session-compact-ops`](../../skills/global/session-compact-ops/SKILL.md) (anotar en `memory/YYYY-MM-DD.md`).
5. Si no hay trabajo accionable: `HEARTBEAT_OK`.

## Por rol

### `mkt-content`

1. Handoffs abiertos hacia `mkt-content` (schemas `research-to-strategy`, `strategy-to-copy`).
2. Contenido pendiente en Trello / `editorial-calendar due --hours 48`.
3. Producir **una** unidad (copy o brief) y dejar handoff al siguiente (`copy-to-design`).
4. No publicar en redes.

### `mkt-social`

1. Handoffs `copy-to-design` / `design-to-producer` / `producer-to-publisher` abiertos hacia `mkt-social`.
2. Render local (`carousel-render` / `video-compose`) si el payload lo pide.
3. Si asset listo: `approval-gate request` AG-12 y STOP (modo C).
4. Tras `approval-gate check` = approved: `publish-safety check` + `mkt-publish --dry-run` (real solo con token Meta y OK CEO).

### `mkt-analytics` / `mkt-research`

1. Handoffs de research abiertos.
2. `competitor-intel viral-analyze --dossier <id> --dry-run` si toca revisión.
3. `social-metrics pull --dossier <id> --dry-run` si faltan Insights reales.
4. Entregar hallazgos vía handoff `research-to-strategy`.

### `mkt-ads`

1. Revisar campañas activas / presupuestos solo si el dossier tiene ads contratados.
2. No lanzar ads sin AG correspondiente (APPROVAL_GATES).
3. Si no hay trabajo: `HEARTBEAT_OK`.

### `mkt-email`

1. Secuencias / newsletters pendientes del dossier.
2. No enviar campañas masivas sin gate.
3. Si no hay trabajo: `HEARTBEAT_OK`.

## Reglas

- Horario activo: 09:00–22:00 America/Caracas (alineado a `heartbeat.activeHours` en plantilla).
- Si no hay nada: `HEARTBEAT_OK`.
- **Nunca** publicar en IG/FB/TikTok/X sin `approval-gate` approved (AG-12) y, si hay IA generativa, AG-13.
- Anotar hallazgos en `memory/YYYY-MM-DD.md` del workspace marketing.
- Dispatcher: `scripts/marketing-dispatch.sh` puede despertar turnos; respeta el mismo STOP en gates.
