# Skills del workspace Jarvis (`agents/jarvis`)

OpenClaw usa como **workspace** de este agente la carpeta `agents/jarvis` (ver `workspace` en `~/.openclaw/openclaw.json`). Los skills compartidos viven aqui:

**Ruta canonica:** `skills/<nombre-del-skill>/SKILL.md` (relativa a `agents/jarvis`).

No busques skills en la raiz del monorepo `clawvis-openclaw/` ni en `~/.openclaw/workspace` salvo que el encargo sea otro proyecto.

## Dos capas de skills

| Capa | Mantenimiento | Ejemplos |
|------|---------------|----------|
| **global-sync** | Manifest `.global-sync-manifest` + scripts sync desde [jarvis-skills-library](https://github.com/AIPP/jarvis-skills-library) | `parallel-judge-ops`, `brainstorming-ops`, `llm-as-judge-ops`, `verification-before-completion` |
| **local-only** | Editar directamente en este repo (holding / OpenClaw) | `carousel-ops`, `proposal-ops`, `pipeline-health-ops`, `trello`, `last30days-openclaw` |

Skills **overlay** (p. ej. `brainstorming-ops`): base canónica en `SKILL.md` (generado) + extensiones holding en `OVERLAY.md` (editar solo el overlay).

**Sincronizar globales:**

```bash
JARVIS_SKILLS_LIBRARY=/var/www/html/proyectos/AIPP/jarvis-skills-library \
  ../../scripts/sync-global-skills-from-library.sh
../../scripts/check-global-skills-sync.sh
```

Ver [../../docs/COHERENCIA_RUNTIME_REPO.md](../../docs/COHERENCIA_RUNTIME_REPO.md).

## Skills destacados (local o sync)

| Skill | Archivo |
|-------|---------|
| **carousel-ops** | [carousel-ops/SKILL.md](carousel-ops/SKILL.md) |
| **llm-as-judge-ops** | [llm-as-judge-ops/SKILL.md](llm-as-judge-ops/SKILL.md) (+ [OVERLAY.md](llm-as-judge-ops/OVERLAY.md)) |
| copywriting-ops | [copywriting-ops/SKILL.md](copywriting-ops/SKILL.md) |
| canva (ClawHub) | [canva/SKILL.md](canva/SKILL.md) |
| scenario-analysis-ops | [scenario-analysis-ops/SKILL.md](scenario-analysis-ops/SKILL.md) |
| strategic-briefing-ops | [strategic-briefing-ops/SKILL.md](strategic-briefing-ops/SKILL.md) |

El resto de carpetas en `skills/` siguen el mismo patron (`SKILL.md` dentro de cada una).

**Marketing** (`agents/marketing`) no duplica skills; enlaza a `../jarvis/skills/...` — ver [../marketing/AGENTS.md](../marketing/AGENTS.md).

## Si en tu PC “no existe” carousel-ops

El skill esta en este repo bajo `agents/jarvis/skills/carousel-ops/`. Si en el host del gateway `ls .../skills/carousel-ops` falla, el arbol `jarvis-ecosystem` del usuario **no esta alineado** con el repositorio: sincronizar o usar symlink — ver [../../docs/COHERENCIA_RUNTIME_REPO.md](../../docs/COHERENCIA_RUNTIME_REPO.md) (seccion skills).
