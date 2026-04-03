# clawvis-openclaw

Respaldo unificado del trabajo alrededor de **OpenClaw**, **Jarvis**, **Agent Town** y coordinación local (Scrum / Trello / Discord).

## Estructura del repositorio

| Carpeta | Contenido |
|---------|-----------|
| `jarvis-ecosystem/` | Automations, agents, skills, scripts, docs del ecosistema Jarvis |
| `documentos-jarvis-openclaw/` | Coordinación y notas en `Documentos` (gestión por fecha) |
| `openclaw-state/` | Copia de `~/.openclaw` (config, credenciales, workspace, agents de estado) |
| `agent-town/` | Proyecto Agent Town (Next); `node_modules` y `.next` no se versionan |
| `deploy/systemd/` | Copia de referencia del unit `openclaw-gateway.service` |
| `descargas-openclaw/` | Descargas relacionadas (opcional) |

**Seguridad:** este repo puede contener **secretos**. Debe ser **privado** en GitHub. Los servicios en ejecución siguen usando `~/.jarvis-ecosystem`, `~/.openclaw` y `~/agent-town` en disco; esta copia es para versionado y respaldo.

## Sincronizar desde el equipo (referencia)

Tras cambios locales, desde `~/clawvis-openclaw`: `git add -A`, `git commit`, `git push origin main`.
