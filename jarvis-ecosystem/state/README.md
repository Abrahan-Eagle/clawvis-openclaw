# state/ — capa de coordinacion runtime

Esta carpeta NO se versiona (excepto este README y los placeholders). Vive en `.gitignore` del monorepo.

## Contenido

- `activity-log.jsonl` — append-only, evento por linea. Lo escribe `skills/global/activity-log/`.
- `tasks/<task-id>.json` — estado vigente de cada tarea.
- `handoffs/<handoff-id>.json` — contrato firmado entre agentes.
- `cache/images/` — cache local de imagenes generadas por `image-ai-free` (Pollinations) para evitar regenerar.

## Como se inicializa

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
mkdir -p state/tasks state/handoffs state/cache/images
touch state/activity-log.jsonl
```

(El skill `activity-log` lo hace automaticamente cuando recibe el primer evento.)

## Como se purga

- Mensual: rotar `activity-log.jsonl` a `state/archive/activity-log-YYYY-MM.jsonl.gz`.
- Tareas con `status=done` se mueven a `state/tasks/_archive/` cada lunes.
- `state/cache/images/` se vacia cuando supera 500MB.

## Privacidad

- No guardar PII en `payload`: solo referencias por `dossier_id`.
- No guardar tokens / API keys.
- Para datos sensibles, el `payload` referencia archivos en `client-dossiers/<id>/`.

Detalle en [docs/COORDINACION_AGENTES.md](../docs/COORDINACION_AGENTES.md) §9.
