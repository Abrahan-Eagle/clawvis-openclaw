## Overlay clawvis — holding OpenClaw

### Destino aprendizajes

Tras tareas significativas del holding:

- Actualizar `LESSONS.md` del workspace jarvis cuando el CEO corrija comportamiento
- Patrones reutilizables → notificar actualización de `SOUL.md` / `AGENTS.md` si aplica
- Complementa `MEMORY.md` y dossiers; no sustituye Trello como registro formal de entregables

### Learning loop HITL (jul 2026)

Cadencia sugerida: **cierre de módulo** o **semanal**.

```bash
cd jarvis-ecosystem
bash scripts/lessons-scan.sh          # candidatos L0XX desde activity-log (solo imprime)
bash scripts/memory-consolidate.sh --agent jarvis   # propuestas memory.json (HITL)
# Con OK CEO: copiar filas a LESSONS.md; memory-consolidate --apply solo si revisado
```

No auto-escribir `LESSONS.md`. Instincts ECC / hooks no aplican en OpenClaw (ver RECURSOS §2.7).

### Integración

Coordinar con `strategic-briefing-ops`, `session-compact-ops` y heartbeat semanal.
