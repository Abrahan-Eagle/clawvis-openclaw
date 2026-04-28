---
name: activity-log
description: "Log unificado de actividad de agentes (state/activity-log.jsonl, tasks/, handoffs)."
metadata:
  version: "1.0.0"
---

# activity-log — log unificado de actividad de agentes

**Tipo:** skill global (no per-agente).
**Ubicacion:** `skills/global/activity-log/`.
**Bin:** `skills/global/activity-log/bin/activity-log`.
**Estado:** v1 (Fase 1 de [docs/PROPUESTA_MEJORA_JARVIS_V2.md](../../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Skill bash + jq que escribe un evento por linea en `state/activity-log.jsonl` y mantiene `state/tasks/<task-id>.json` con el estado vigente. Es la fuente de verdad operativa del ecosistema.

Documento de contrato: [docs/COORDINACION_AGENTES.md](../../../docs/COORDINACION_AGENTES.md).

## Por que

Hasta hoy los agentes no tenian un log unificado. Trello + Notion + `MEMORY.md` funcionan a medias y exigen que alguien lo escriba. Este skill hace que **cualquier agente** registre inicio/fin/handoffs/eventos con un comando determinista.

## Variables de entorno

| Variable | Default | Proposito |
|---|---|---|
| `JARVIS_STATE_DIR` | `<repo_root>/state` | Donde viven `activity-log.jsonl` y `tasks/` |
| `JARVIS_DOSSIERS_DIR` | `<repo_root>/client-dossiers` | Para validar `--dossier` en `start` |

`<repo_root>` se detecta con `git rev-parse --show-toplevel` o como dos niveles arriba del bin si no hay git.

## Comandos

### `start` — abrir tarea

```bash
activity-log start \
  --agent mkt-content \
  --title "Carrusel IG lanzamiento" \
  --dossier cli-DEMO-rrss \
  --ref carousel \
  [--task task-explicit-id]
```

Crea `state/tasks/<task-id>.json` y emite evento `type=start`. Si `--dossier` apunta a un id que no existe en `client-dossiers/`, **falla con codigo 2** (validacion de dossier obligatorio).

Salida (stdout, JSON): `{ "task_id": "task-..." }`.

### `end` — cerrar tarea

```bash
activity-log end --task task-...-abcd [--note "entregado"]
```

Marca la tarea `done`, emite evento `type=end`. Si tiene handoffs abiertos, advierte por stderr.

### `event` — hito sin cambio de estado

```bash
activity-log event \
  --agent mkt-content \
  --task task-... \
  --kind progress|info|warn \
  --note "5 de 10 slides listos" \
  [--payload-file /tmp/extra.json]
```

### `block` / `resume`

```bash
activity-log block --task ... --reason "espera brand kit"
activity-log resume --task ...
```

### `handoff` — registrar handoff (lo invoca el skill `handoff` automaticamente)

```bash
activity-log handoff \
  --task task-... \
  --from mkt-content \
  --to mkt-social \
  --handoff-id handoff-... \
  --kind create|accept|reject \
  [--reason "..."]
```

### `tail`

```bash
activity-log tail --n 30
```

### `filter`

```bash
activity-log filter --agent mkt-content
activity-log filter --dossier cli-DEMO-rrss
activity-log filter --task task-... --since 2026-04-26
activity-log filter --type handoff --status open
```

Salida: lineas JSONL (compatibles con `jq`).

### `tasks` — listar tareas vivas

```bash
activity-log tasks --status in_progress
activity-log tasks --agent mkt-content
activity-log tasks --dossier cli-DEMO-rrss
```

## Formato de evento

Cada linea de `state/activity-log.jsonl`:

```json
{"ts":"2026-04-27T10:30:00Z","agent":"mkt-content","type":"start","task_id":"task-20260427-103000-ab","dossier_id":"cli-DEMO-rrss","ref":"carousel","actor":"agent","payload":{"title":"Carrusel IG lanzamiento"}}
```

Tipos validos: `start`, `end`, `event`, `handoff`, `block`, `resume`, `dossier-warn`.

## Integracion en SOUL.md de cada agente

```markdown
- Coordinacion operativa: registra `activity-log start` al iniciar tarea relevante, `event` para hitos, `handoff create` al pasar a otro agente, `activity-log end` al cerrar. Detalle: [docs/COORDINACION_AGENTES.md](../../docs/COORDINACION_AGENTES.md).
```

## Limites

- No es un broker: no emite notificaciones push. El skill `coordinator` ofrece `status` y la automation `coordination-pulse` lo publica.
- No bloquea operaciones del agente: si el log falla por disco lleno, registra error a stderr pero no aborta la tarea. La filosofia es **best-effort tracking**.
- No reemplaza Trello: Trello sigue siendo la vista humana del flujo. `activity-log` es el log maquinal.

## Dependencias

- `bash`, `jq`, `coreutils`. Sin paquetes externos.

## Tests rapidos

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
bin=skills/global/activity-log/bin/activity-log
TASK=$($bin start --agent demo --title "prueba" --ref test | jq -r .task_id)
$bin event --agent demo --task "$TASK" --kind progress --note "midcheck"
$bin end --task "$TASK"
$bin tail --n 5
$bin tasks --status done
```
