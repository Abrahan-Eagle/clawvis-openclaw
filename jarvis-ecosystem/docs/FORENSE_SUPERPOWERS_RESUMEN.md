# Forense Superpowers — Resumen de patrones adoptados

**Repo analizado:** [obra/superpowers](https://github.com/obra/superpowers) (152k stars, MIT)  
**Fecha del analisis:** abril 2026  
**Objetivo:** Extraer patrones de metodologia de desarrollo y operaciones para fortalecer OpenClaw/Jarvis.

---

## Que es Superpowers

Superpowers es un framework de skills composables para agentes de IA que impone una metodologia de trabajo rigurosa. Su flujo completo:

1. **Brainstorming** — explorar idea, preguntar, proponer alternativas, obtener aprobacion
2. **Writing plans** — descomponer en tareas bite-sized de 2-5 min con codigo completo
3. **Git worktrees** — aislamiento de features en branches separadas
4. **Subagent-driven development** — un subagente por tarea + revision en 2 fases
5. **TDD** — test first, watch fail, minimal code, watch pass, refactor
6. **Code review** — entre cada tarea (spec compliance + code quality)
7. **Verification before completion** — evidencia antes de claims
8. **Systematic debugging** — 4 fases, root cause antes de fix
9. **Finishing branch** — verificar tests, presentar opciones (merge/PR/keep/discard)

## Que se adopto (dentro de OpenClaw/Jarvis)

| Concepto Superpowers | Implementacion | Archivos |
|---|---|---|
| **Brainstorming obligatorio** | Skill adaptado a operaciones (propuestas, campanas, features, config) | `skills/brainstorming-ops/SKILL.md` |
| **Verificacion antes de completar** | Skill con tabla de claims vs evidencia para cada tipo de tarea del ecosistema | `skills/verification-before-completion/SKILL.md` |
| **Debugging sistematico** | Skill 4 fases adaptado a problemas del ecosistema (gateway, integraciones, scripts) | `skills/systematic-debugging/SKILL.md` |
| **Dev methodology (TDD + plans + review)** | Skill consolidado para cuando se escriba codigo o se active dev-agency | `skills/dev-methodology/SKILL.md` |
| **Plugin Superpowers** | Instalado en Cursor para uso directo al programar | `~/.cursor/plugins/local/superpowers/` |

## Que NO se adopto (y por que)

| Concepto | Razon |
|----------|-------|
| Git worktrees | Los agentes del ecosistema no trabajan en branches paralelas |
| TDD estricto como Iron Law para ventas/marketing | Solo aplica a codigo, no a operaciones de negocio |
| Plugin marketplace (`/plugin install`) | OpenClaw no tiene marketplace de plugins Superpowers |
| Subagent-driven development literal | Los subagentes de OpenClaw (sales-hunter, mkt-content) no son developers; el patron se adapto conceptualmente |
| Writing-skills (meta-skill para crear skills) | Demasiado especifico para contribuir al repo Superpowers; no necesario internamente |

## Principio aplicado

> "OpenClaw es el centro. Los repos externos son ideas para fortalecer a Jarvis, no para reemplazarlo."

Los skills se crearon como Markdown en el workspace Jarvis, usando el formato nativo de OpenClaw. Los agentes los leen automaticamente al iniciar sesion. No se agrego ninguna dependencia externa ni servidor adicional.

## Archivos creados/modificados

### Archivos nuevos

| Archivo | Descripcion |
|---------|-------------|
| `agents/jarvis/skills/brainstorming-ops/SKILL.md` | Brainstorming adaptado a operaciones |
| `agents/jarvis/skills/verification-before-completion/SKILL.md` | Verificacion obligatoria antes de claims |
| `agents/jarvis/skills/systematic-debugging/SKILL.md` | Debugging en 4 fases |
| `agents/jarvis/skills/dev-methodology/SKILL.md` | TDD + planes + code review + subagentes |
| `docs/FORENSE_SUPERPOWERS_RESUMEN.md` | Este documento |

### Archivos modificados

| Archivo | Cambio |
|---------|--------|
| `agents/jarvis/AGENTS.md` | Seccion "Protocolo de calidad (Superpowers)" |
| `agents/ventas/AGENTS.md` | Seccion "Protocolo de calidad (Superpowers)" con brainstorming + verificacion |
| `agents/marketing/AGENTS.md` | Seccion "Protocolo de calidad (Superpowers)" con brainstorming + verificacion |

### Local (no en Git)

| Ubicacion | Contenido |
|-----------|-----------|
| `~/.cursor/plugins/local/superpowers/` | Plugin Superpowers completo (git clone) |

## Nota sobre dev-agency

`dev-agency` esta en estado "Planificada" en `COMPANIES.md`. Cuando se active, el skill `dev-methodology/SKILL.md` ya contiene la metodologia completa (TDD, planes, code review, subagentes). Solo faltara crear el workspace y los agentes.

## Referencias

- [GOALS.md](../GOALS.md)
- [APPROVAL_GATES.md](APPROVAL_GATES.md)
- [FORENSE_PAPERCLIP_RESUMEN.md](FORENSE_PAPERCLIP_RESUMEN.md) (modulo anterior)
- [Superpowers GitHub](https://github.com/obra/superpowers)
