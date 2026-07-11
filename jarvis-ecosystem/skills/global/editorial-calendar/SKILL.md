# editorial-calendar

**Tipo:** skill global ejecutable.  
**Bin:** `skills/global/editorial-calendar/bin/editorial-calendar`  
**Estado:** v1 (loop RRSS P0)

## Comandos

```bash
editorial-calendar add --dossier corralx --channel instagram --at 2026-07-15T14:00:00Z --asset out/x/01.png
editorial-calendar list --dossier corralx
editorial-calendar due --hours 72
editorial-calendar approve --id slot-...
editorial-calendar set-status --id slot-... --status ready
```

Persistencia: `state/editorial-calendar/slot-*.json`.
