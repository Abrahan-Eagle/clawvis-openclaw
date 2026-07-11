---
name: judge-run
description: >-
  Eval ligero pre-AG-12: checklist heurística + plantilla LLM; escribe
  state/judge/judge-*.json consumible por JMC GET /v1/judge/last.
---

# judge-run

**Bin:** `skills/global/judge-run/bin/judge-run`  
**Estado:** v1 (jul 2026)

```bash
judge-run --handoff handoff-20260427-150839-63c776 --category carousel_ig
judge-run --file state/handoffs/handoff-….json --category generic
```

Salida: `state/judge/judge-<ts>-<id>.json` + JSON resumen en stdout.

Integrar **antes** de `approval-gate request` AG-12. Ver `docs/APPROVAL_GATES.md` y `docs/MANUAL_RRSS_JARVIS.md`.

Complementa `llm-as-judge-ops` (rúbrica en sesión); no sustituye al CEO.
