# state/ — capa de coordinacion runtime

Esta carpeta NO se versiona (excepto este README y los placeholders). Vive en `.gitignore` del monorepo.

## Contenido

- `activity-log.jsonl` — append-only, evento por linea. Lo escribe `skills/global/activity-log/`.
- `tasks/<task-id>.json` — estado vigente de cada tarea.
- `handoffs/<handoff-id>.json` — contrato firmado entre agentes.
- `approvals/esc-*.json` — gates AG-12/13 (`approval-gate`).
- `judge/judge-*.json` — eval pre-AG-12 (`judge-run`); consumido por JMC `/v1/judge/last`.
- `editorial-calendar/slot-*.json` — calendario RRSS.
- `publish-log/`, `publish-safety/` — intentos y pre-flight de publicación.
- `metrics/<dossier>/YYYY-MM.json` — Insights (`social-metrics`).
- `reports/<dossier>/report-*.html` — informes cliente.
- `competitor-intel/<dossier>/` — posts ingestados / análisis.
- `cache/images/` — cache local de imagenes generadas por `image-ai-free` (Pollinations) para evitar regenerar.

## Como se inicializa

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
mkdir -p state/tasks state/handoffs state/approvals state/judge state/editorial-calendar state/cache/images
touch state/activity-log.jsonl
```

(El skill `activity-log` y los CLIs RRSS crean subdirs al primer uso.)

Loop operativo: [docs/MANUAL_RRSS_JARVIS.md](../docs/MANUAL_RRSS_JARVIS.md).

## Como se purga

- Mensual: rotar `activity-log.jsonl` a `state/archive/activity-log-YYYY-MM.jsonl.gz`.
- Tareas con `status=done` se mueven a `state/tasks/_archive/` cada lunes.
- `state/cache/images/` se vacia cuando supera 500MB.

## Privacidad

- No guardar PII en `payload`: solo referencias por `dossier_id`.
- No guardar tokens / API keys.
- Para datos sensibles, el `payload` referencia archivos en `client-dossiers/<id>/`.

Detalle en [docs/COORDINACION_AGENTES.md](../docs/COORDINACION_AGENTES.md) §9.
