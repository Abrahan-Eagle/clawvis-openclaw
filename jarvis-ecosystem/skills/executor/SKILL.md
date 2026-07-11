---
name: executor
description: "Ejecutor de planes JSON: dry-run por defecto; --live invoca CLIs allowlisted (nunca mkt-publish --force-live)."
metadata:
  version: "2.0.0"
---

# executor

> Inspiración: Jarvis-MK37 executor — **v2** ejecuta skills CLI locales allowlisted; no genera código arbitrario ni llama al gateway.

## Uso

```bash
./bin/planner "mi objetivo" > /tmp/plan.json
# Editar steps: tool=editorial-calendar|handoff|approval-gate|... action=... args={...}
./bin/executor /tmp/plan.json          # dry-run
./bin/executor --live /tmp/plan.json   # ejecuta bins allowlisted
```

## Allowlist (relativa a jarvis-ecosystem)

`editorial-calendar`, `approval-gate`, `client-onboard`, `mkt-publish` (sin `--force-live`), `handoff`, `activity-log`, `coordinator`, `publish-safety`, `creative-qa`, `de-ai-ify`, `competitor-intel`, `client-report`, `social-metrics`, `brand-kit`, `carousel-render`, `error-recovery`.

**Gates:** publicación real (`mkt-publish --force-live`) queda fuera del executor — solo manual tras AG-12.
