# Context pack — REVIEW

> Activar con `JARVIS_CONTEXT_MODE=review` o *«modo review»*.

## Priorizar

- `judge-run` + `llm-as-judge-ops` / `parallel-judge-ops` si alto riesgo
- `creative-qa`, `publish-safety`, `verification-before-completion`
- `approval-gate check` / `list --status pending`
- `social-metrics` / `client-report` en dry-run si toca cierre

## No hacer

- No reescribir creatividades desde cero (devolver a modo produce)
- No `approve` gates sin ser el CEO / sin evidencia
- No merge/push ni cambios `openclaw.json` (AG-07)

## Presupuesto de contexto

- 1 handoff + 1 judge JSON + checklist corta
- Rúbrica holding en `llm-as-judge-ops/OVERLAY.md`

## Compact

Tras review: anotar veredicto en `memory/YYYY-MM-DD.md`; candidatos a lección → `scripts/lessons-scan.sh`
