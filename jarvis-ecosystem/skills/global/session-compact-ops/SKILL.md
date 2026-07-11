---
name: session-compact-ops
description: >-
  Compactación estratégica de sesión (estilo ECC strategic-compact, adaptado a
  OpenClaw holding): cuándo resumir, plantilla, escritura a memory/YYYY-MM-DD.md
  + memory-store trim. Sin hooks ECC; convive con compaction.memoryFlush nativo.
---

# session-compact-ops

**Tipo:** protocolo (sin bin propio).  
**Complementa:** `agents.defaults.compaction.memoryFlush` en OpenClaw (ya enabled en plantilla).  
**No es:** plugin ECC ni hook SessionStart/Stop de Claude Code.

## Cuándo compactar (triggers)

Ejecutar el protocolo cuando ocurra **cualquiera**:

1. **Fin de fase** — cerraste un pipeline (research→copy→design→publisher) o un módulo documentado.
2. **~N acciones tool** — tras ~15–25 tool calls sustanciales en la misma sesión (o contexto cerca del límite).
3. **Pre-gate AG** — antes de `approval-gate request` (AG-12/13/03) o escalación async.
4. **Pre-handoff** — antes de `handoff create` hacia otro agente / unidad.
5. **Pre-handoff humano** — antes de compactar chat o traspasar a otro agente Cursor (`handoff` skill).

Si OpenClaw ya disparó `memoryFlush`, **no dupliques** el mismo resumen: lee el daily file y solo añade lo que falte.

## Plantilla de resumen (escribir)

Crear o anexar en `agents/<workspace>/memory/YYYY-MM-DD.md`:

```markdown
## Compact — HH:MM UTC

- **Objetivo sesión:** …
- **Hecho:** (3–7 bullets)
- **Decisiones:** …
- **Pendiente / blocked:** …
- **Gates tocados:** AG-… / ninguno
- **Handoffs / task_ids:** …
- **Próximo paso único:** …
```

Luego:

```bash
# Recortar memoria estructurada si creció
memory-store --file agents/<agent>/memory.json trim
# Opcional: consolidar propuestas HITL
scripts/memory-consolidate.sh --agent <agent>
```

## Qué NO hacer

- No volcar transcripts enteros ni secretos/tokens.
- No compactar solo para “hacer ruido” en heartbeats — si no hay sustancia: `HEARTBEAT_OK`.
- No sustituir `LESSONS.md` (usar `scripts/lessons-scan.sh` + OK CEO).

## Referencias

- Memoria nativa + MemPalace: `docs/MEMORIA_MEMPALACE.md`
- Core prompt: `skills/global/core-prompt.md` (§ Context packs + compact)
- Marketing heartbeat: `agents/marketing/HEARTBEAT.md`
