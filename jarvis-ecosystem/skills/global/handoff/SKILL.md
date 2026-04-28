# handoff — contratos de paso entre agentes

**Tipo:** skill global.
**Ubicacion:** `skills/global/handoff/`.
**Bin:** `skills/global/handoff/bin/handoff`.
**Estado:** v1 (Fase 1 de [PROPUESTA_MEJORA_JARVIS_V2.md](../../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Skill bash + jq que crea, acepta y rechaza handoffs JSON entre agentes. Cada handoff se valida contra un schema JSON Schema (subset) en `schemas/`. Cada accion emite tambien un evento `type=handoff` en el `activity-log`.

Detalle de contrato: [docs/COORDINACION_AGENTES.md](../../../docs/COORDINACION_AGENTES.md).

## Schemas disponibles

| Schema | De | A | Proposito |
|---|---|---|---|
| `research-to-strategy.json` | mkt-analytics, sales-hunter | mkt-content, sales-closer | Audiencia, competencia, oportunidades, fuentes |
| `strategy-to-copy.json` | mkt-content (estratega) | mkt-content (copy) | Brief creativo, mensajes clave, voz, KPI |
| `copy-to-design.json` | mkt-content | mkt-social, carousel-render, video-short | Hook, slides JSON, CTA, formato deliverable |
| `design-to-producer.json` | mkt-social | video-short, carousel-render | Plantilla, brand kit, voz, musica, duracion |
| `producer-to-publisher.json` | video-short, carousel-render | mkt-social, jarvis | Asset final + metadata + AG-12 status |

## Comandos

### `create`

```bash
handoff create \
  --from mkt-content \
  --to mkt-social \
  --schema copy-to-design \
  --task task-...-abcd \
  --payload-file /tmp/payload.json
```

Valida `--payload-file` contra `schemas/copy-to-design.json`. Si pasa:
- Crea `state/handoffs/handoff-...-id.json`.
- Llama internamente a `activity-log handoff --kind create`.
- Imprime en stdout `{ "handoff_id": "..." }`.

Si falla la validacion, devuelve codigo 3 con mensaje del campo invalido.

### `accept`

```bash
handoff accept --id handoff-... --by mkt-social [--note "..."]
```

Marca aceptado y emite evento. El receptor confirma que recibio y que va a procesar.

### `reject`

```bash
handoff reject --id handoff-... --by mkt-social --reason "falta brand kit"
```

### `list`

```bash
handoff list --open
handoff list --to mkt-social --open
handoff list --task task-...-abcd
handoff list --schema copy-to-design
```

### `show`

```bash
handoff show --id handoff-...
```

### `validate-payload`

```bash
handoff validate-payload --schema copy-to-design --payload-file /tmp/p.json
```

(Util para testear payloads antes de crear el handoff.)

## Validacion (subset JSON Schema)

El validador `bin/handoff` implementa un subset minimo en jq:

- `required: [..]` — todos los campos deben existir y no ser null/empty.
- `type: string|number|integer|array|object|boolean` — chequeo basico.
- `enum: [..]` — restringe valores literales.

No es JSON Schema completo (sin `$ref`, `anyOf`, `oneOf`, formats). Si necesitas validacion mas estricta, instalar `ajv-cli` (Node) o `python -m jsonschema` y reemplazar el validador.

## Variables de entorno

| Variable | Default | Proposito |
|---|---|---|
| `JARVIS_STATE_DIR` | `<repo>/state` | Donde se guardan handoffs |
| `JARVIS_SKILLS_DIR` | autodetect | Donde encontrar `activity-log` |

## Limites

- Si dos procesos crean handoffs en paralelo, no hay file lock; en este monorepo de bajo trafico es aceptable. Si se vuelve hot path, añadir `flock` a `state/.lock`.
- Schemas son contratos minimos; no impiden que el payload tenga campos extra. Filosofia: contrato como red de seguridad, no camisa de fuerza.

## Tests rapidos

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
bin=skills/global/handoff/bin/handoff
log=skills/global/activity-log/bin/activity-log

TASK=$($log start --agent mkt-content --title "Demo handoff" --ref test | jq -r .task_id)
cat > /tmp/p.json <<JSON
{
  "hook": "El error #1 que cuesta clientes",
  "slides": [{"type":"hook","title":"H","subtitle":"S"}],
  "cta": "DM o link en bio",
  "deliverable_format": "carousel_ig_1080x1350"
}
JSON
HID=$($bin create --from mkt-content --to mkt-social --schema copy-to-design --task "$TASK" --payload-file /tmp/p.json | jq -r .handoff_id)
echo "Handoff: $HID"
$bin list --open
$bin accept --id "$HID" --by mkt-social --note "todo ok"
$log end --task "$TASK"
```
