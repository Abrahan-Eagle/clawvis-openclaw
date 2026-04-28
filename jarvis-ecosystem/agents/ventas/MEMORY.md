# MEMORY.md — Ventas (memoria a largo plazo)

**Memoria estructurada (máquina):** [`memory.json`](memory.json) — skill [`../../skills/global/memory-store/`](../../skills/global/memory-store/). **Este archivo** = notas y registro en prosa; el JSON alimenta el contexto compacto en sesión.

Solo lectura/escritura en **sesion principal** con el humano (ver [AGENTS.md](AGENTS.md)).

Este archivo es el equivalente de [../jarvis/MEMORY.md](../jarvis/MEMORY.md) para el **workspace Ventas**: decisiones de pipeline, acuerdos con el CEO/supervisor, notas que no deben perderse entre sesiones.

- Si aun no hay entradas, dejar esta seccion vacia o anotar la fecha de creacion del archivo.

## Autonomía

- **autonomy_mode:** `D` (documental; alinear con `JARVIS_AUTONOMY_MODE` en `~/.openclaw/.env` cuando exista).
- Docs: [AUTONOMIA_MODOS](../../docs/AUTONOMIA_MODOS.md), [ESCALACION_ASYNC](../../docs/ESCALACION_ASYNC.md).

---

## Registro (editar segun avance el equipo)

*(Sin entradas aun — el agente puede anadir bullets con fecha cuando el superusuario lo pida.)*
