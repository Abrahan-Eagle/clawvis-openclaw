# Skills del workspace Jarvis (`agents/jarvis`)

OpenClaw usa como **workspace** de este agente la carpeta `agents/jarvis` (ver `workspace` en `~/.openclaw/openclaw.json`). Los skills compartidos viven aqui:

**Ruta canonica:** `skills/<nombre-del-skill>/SKILL.md` (relativa a `agents/jarvis`).

No busques skills en la raiz del monorepo `clawvis-openclaw/` ni en `~/.openclaw/workspace` salvo que el encargo sea otro proyecto; para carruseles y Canva el skill es:

| Skill | Archivo |
|-------|---------|
| **carousel-ops** | [carousel-ops/SKILL.md](carousel-ops/SKILL.md) |
| copywriting-ops | [copywriting-ops/SKILL.md](copywriting-ops/SKILL.md) |
| canva (ClawHub) | [canva/SKILL.md](canva/SKILL.md) |
| scenario-analysis-ops | [scenario-analysis-ops/SKILL.md](scenario-analysis-ops/SKILL.md) |
| strategic-briefing-ops | [strategic-briefing-ops/SKILL.md](strategic-briefing-ops/SKILL.md) |

El resto de carpetas en `skills/` siguen el mismo patron (`SKILL.md` dentro de cada una).

**Marketing** (`agents/marketing`) no duplica skills; enlaza a `../jarvis/skills/...` — ver [../marketing/AGENTS.md](../marketing/AGENTS.md).

## Si en tu PC “no existe” carousel-ops

El skill esta en este repo bajo `agents/jarvis/skills/carousel-ops/`. Si en el host del gateway `ls .../skills/carousel-ops` falla, el arbol `jarvis-ecosystem` del usuario **no esta alineado** con el repositorio: sincronizar o usar symlink — ver [../../docs/COHERENCIA_RUNTIME_REPO.md](../../docs/COHERENCIA_RUNTIME_REPO.md) (seccion skills).
