# Forense oh-my-claudecode (OMC) — Resumen

*Modulo completado: abril 2026*

## Repo analizado

| Repo | Stars | Foco |
|------|-------|------|
| [yeachan-heo/oh-my-claudecode](https://github.com/yeachan-heo/oh-my-claudecode) | 28.8k | Multi-agent orchestration para Claude Code. 29 agentes especializados, 32 skills, team pipeline (plan-prd-exec-verify-fix), OpenClaw bridge, deep interview (Socratic questioning), learner (skill extraction), git trailers (structured commits). |

## Patron clave adoptado: Task Pipeline + Deep Interview

OMC tiene un pipeline formalizado para tareas multi-paso (plan -> prd -> exec -> verify -> fix) con un gate de entrevista socratica antes de ejecutar. Adaptamos ambos patrones al ecosistema Jarvis para dar estructura a tareas complejas y asegurar que los requisitos sean claros antes de invertir esfuerzo.

## Que se adopto

| Skill | Fuente en OMC | Ubicacion | Agentes que lo usan |
|-------|---------------|-----------|---------------------|
| **deep-interview-ops** | skills/deep-interview (Socratic questioning + ambiguity gating) | `agents/jarvis/skills/deep-interview-ops/SKILL.md` | sales-hunter, mkt-content, jarvis |
| **task-pipeline-ops** | Team pipeline (plan-prd-exec-verify-fix) | `agents/jarvis/skills/task-pipeline-ops/SKILL.md` | jarvis (coordinacion) |
| **structured-commits-ops** | CLAUDE.md git trailers section | `agents/jarvis/skills/structured-commits-ops/SKILL.md` | jarvis, dev-agency |
| **session-learner-ops** | skills/learner (pattern extraction) | `agents/jarvis/skills/session-learner-ops/SKILL.md` | jarvis |
| **verification sizing + frescura** | AGENTS.md verification protocol | Mejora a `verification-before-completion/SKILL.md` | Todos |

## Que NO se adopto (y por que)

| Patron | Fuente en OMC | Razon |
|--------|---------------|-------|
| OMC runtime/CLI/plugin | Todo el paquete npm | Es para Claude Code CLI, no para Cursor + OpenClaw |
| tmux workers (omc team) | src/cli/team.ts | Implementacion atada a Claude Code terminal |
| Codex/Gemini multi-model | ccg, ask providers | Jarvis usa Cursor (auto) + Ollama, diferente ecosistema |
| Hook scripts Node.js | hooks/*.mjs | Claude Code lifecycle, Jarvis usa OpenClaw hooks |
| HUD statusline | skills/hud/ | UI de terminal OMC, Jarvis usa Discord/Trello |
| Magic keyword detection | keyword-detector hook | Procesamiento de prompts de Claude Code, no aplica |
| .omc/ state directory | State management | Acoplado a sesiones OMC, Jarvis tiene MemPalace/Trello |
| LSP/AST tools | lsp_*, ast_grep_* | Dev tools, solo relevantes para dev-agency futura |
| Code simplifier | code-simplifier.mjs | Solo desarrollo |
| Visual verdict | skills/visual-verdict/ | QA de screenshots, solo desarrollo |
| Ralph/Ultrawork persistence | skills/ralph/, ultrawork/ | Loops de persistencia de Claude Code sessions |
| Anti-slop cleaner | skills/ai-slop-cleaner/ | Limpieza de patrones IA en codigo, solo dev |
| Notepad/Project Memory | .omc/notepad.md | Jarvis ya tiene MemPalace + MEMORY.md |

## Archivos creados / modificados

**Creados:**
- `agents/jarvis/skills/deep-interview-ops/SKILL.md` — cuestionamiento socratico, 6 dimensiones, gate de claridad
- `agents/jarvis/skills/task-pipeline-ops/SKILL.md` — pipeline plan-spec-exec-verify-fix
- `agents/jarvis/skills/structured-commits-ops/SKILL.md` — git trailers con decision metadata
- `agents/jarvis/skills/session-learner-ops/SKILL.md` — extraccion de patrones con 4 quality gates
- `docs/FORENSE_OMC_RESUMEN.md` — este archivo

**Modificados:**
- `agents/jarvis/skills/verification-before-completion/SKILL.md` — agregado sizing tiers y regla de frescura
- `agents/jarvis/AGENTS.md` — seccion "Protocolo de calidad" ampliada con skills OMC
- `agents/ventas/AGENTS.md` — deep-interview-ops agregado al protocolo de calidad
- `agents/marketing/AGENTS.md` — deep-interview-ops agregado al protocolo de calidad
- `agents/jarvis/MEMORY.md` — log de decisiones
- `docs/OPERACION_POST_GOBIERNO.md` — enlace al modulo
- `docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md` — seccion de respaldo

## Impacto en el ecosistema

1. **Claridad antes de accion:** deep-interview-ops asegura que los requisitos sean claros (scoring >= 3.5/5) antes de invertir esfuerzo en propuestas o campanas.
2. **Consistencia en tareas complejas:** task-pipeline-ops da una secuencia repetible (plan-spec-exec-verify-fix) para trabajo multi-paso.
3. **Historial de decisiones:** structured-commits-ops crea un log de decisiones accesible via `git log` con trailers estandarizados.
4. **Mejora continua:** session-learner-ops extrae patrones concretos de tareas completadas para alimentar futuras operaciones.
5. **Verificacion proporcional:** sizing tiers evitan tanto la sub-verificacion como la sobre-verificacion.
