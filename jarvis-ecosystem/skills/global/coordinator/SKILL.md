# coordinator — sintesis del estado del ecosistema

**Tipo:** skill global.
**Bin:** `skills/global/coordinator/bin/coordinator`.
**Estado:** v1 (Fase 2 de [docs/PROPUESTA_MEJORA_JARVIS_V2.md](../../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Skill que lee `state/activity-log.jsonl`, `state/tasks/`, `state/handoffs/` y `client-dossiers/` y entrega un resumen ejecutivo legible:

- Quien tiene tareas activas y cuantas.
- Que handoffs estan abiertos (creados pero no aceptados/rechazados).
- Que tareas estan atrancadas (>N horas sin evento).
- Que dossiers estan huerfanos (existen pero ningun evento reciente los toca).

Lo invoca Jarvis manualmente (cuando lo pide el superusuario) o el cron `coordination-pulse.yaml` cada 4 horas.

## Comandos

### `status` — resumen general

```bash
coordinator status
```

Salida (texto humano):

```
Ecosistema Jarvis — pulso de coordinacion (2026-04-27 14:30 UTC)

Tareas activas: 3
  - mkt-content     1  (Carrusel IG cli-DEMO-rrss)
  - sales-closer    1  (Propuesta cli-acme)
  - dev-agency      1  (Bug fix cli-omc)

Handoffs abiertos: 2
  - handoff-...-ab  copy-to-design   mkt-content -> mkt-social  hace 2h
  - handoff-...-cd  research-to-strategy  mkt-analytics -> mkt-content  hace 5h (>4h)

Tareas atrancadas (>24h sin evento): 1
  - task-...-xy  sales-account  cli-acme  ultimo evento hace 36h

Dossiers huerfanos (sin actividad >7 dias): 0
```

### `status --json`

Mismo contenido en JSON estructurado (para consumir desde `coordination-pulse.yaml`).

### `status --agent <name>`

Detalle solo de un agente: tareas activas, handoffs entrantes/salientes, ultimas N actividades.

### `stuck`

```bash
coordinator stuck --hours 24
```

Lista tareas vivas cuyo ultimo evento es anterior a `now - hours`.

### `summary --dossier <id>`

```bash
coordinator summary --dossier cli-DEMO-rrss
```

Cronologia de todos los eventos asociados al dossier.

### `next --agent <name>`

Heuristica simple: dado el agente, sugiere accion siguiente:

- Si tiene handoff entrante abierto >2h → "aceptar o rechazar handoff X".
- Si tiene tarea blocked >12h → "resume o escalar".
- Si no tiene tareas → "leer cola en Trello / dossier".

Esto es heuristica, no IA. La idea es marcar siguientes pasos visibles, no decidir por el agente.

### `dossiers --orphan-days N`

Lista dossiers sin actividad en N dias.

## Variables de entorno

| Variable | Default | Proposito |
|---|---|---|
| `JARVIS_STATE_DIR` | `<repo>/state` | Para localizar log + tasks + handoffs |
| `JARVIS_DOSSIERS_DIR` | `<repo>/client-dossiers` | Para detectar dossiers huerfanos |

## Limites

- No tiene memoria propia: cada llamada relee todo. Para `state/activity-log.jsonl` con >100k lineas, conviene rotar mensual.
- No envia notificaciones por si solo: la automation `coordination-pulse.yaml` es la que publica.
- Las heuristicas de `next` son simples; no reemplazan juicio humano.

## Tests rapidos

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
bin=skills/global/coordinator/bin/coordinator
$bin status
$bin status --json | jq .
$bin stuck --hours 1
$bin summary --dossier cli-DEMO-rrss
$bin next --agent mkt-content
$bin dossiers --orphan-days 7
```
