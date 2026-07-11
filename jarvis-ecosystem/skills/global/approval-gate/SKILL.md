# approval-gate

**Tipo:** skill global ejecutable.  
**Bin:** `skills/global/approval-gate/bin/approval-gate`  
**Estado:** v1 (loop RRSS P0)

Gates AG-12 / AG-13 / AG-03 persistidos en `state/approvals/esc-*.json`.  
El dispatcher y `mkt-publish` deben exigir `status=approved` antes de publicar.

```bash
approval-gate request --ag AG-12 --task task-... --handoff handoff-... --dossier corralx
approval-gate approve --id esc-...
approval-gate check --handoff handoff-...
approval-gate list --status pending
```
