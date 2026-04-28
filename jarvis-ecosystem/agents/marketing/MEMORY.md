# MEMORY.md — Marketing (memoria a largo plazo)

**Memoria estructurada (máquina):** [`memory.json`](memory.json) — skill [`../../skills/global/memory-store/`](../../skills/global/memory-store/). **Este archivo** = notas y registro en prosa; el JSON alimenta el contexto compacto en sesión.

Solo lectura/escritura en **sesion principal** con el humano (ver [AGENTS.md](AGENTS.md)).

Este archivo es el equivalente de [../jarvis/MEMORY.md](../jarvis/MEMORY.md) para el **workspace Marketing**: campanas, clientes, acuerdos con CEO/supervisor, notas que no deben perderse entre sesiones.

- Si aun no hay entradas, dejar esta seccion vacia o anotar la fecha de creacion del archivo.

## Autonomía

- **autonomy_mode:** `D` (documental; alinear con `JARVIS_AUTONOMY_MODE` en `~/.openclaw/.env` cuando exista).
- Docs: [AUTONOMIA_MODOS](../../docs/AUTONOMIA_MODOS.md), [ESCALACION_ASYNC](../../docs/ESCALACION_ASYNC.md).

---

## Registro (editar segun avance el equipo)

- **2026-04-28 (pm):** **Adaptación v2** de las 40 skills: cuerpo ES dossier-first, hooks pipeline (`brand-kit`, `carousel-render`, `tts-free`, …), coordinación con comandos reales, upstream en `references/upstream-en.md`. Generador: `scripts/generate_marketing_skills.py` → `marketing_skills_v2/`. Fichas: `scripts/marketing_skills_data/*.yaml`. Sync runtime: `scripts/sync-marketing-skills-from-repo.sh`. Índice: `skills/README.md`. Investigación: `docs/RESEARCH_MARKETING_SKILLS.md`.
