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

## Puesta en marcha (Linux, máquina actual)

1. **Node.js 22+** (OpenClaw lo exige): con nvm, `nvm install 22` y `nvm alias default 22`. En `~/.bashrc` ya se puede cargar `nvm use 22` en silencio tras `nvm.sh`.
2. **OpenClaw global:** `npm install -g openclaw@latest` usando el Node 22 de nvm.
3. **Config en vivo:** copiar o enlazar `~/.openclaw` desde `openclaw-state/` y ajustar rutas (`/home/TU_USUARIO`). En el navegador embebido, `browser.executablePath` debe apuntar a un Chrome/Chromium instalado (ej. `/usr/bin/google-chrome`).
4. **Ecosistema Jarvis:** `ln -sfn /ruta/al/repo/jarvis-ecosystem ~/.jarvis-ecosystem`.
5. **Gateway (systemd usuario):** copiar `deploy/systemd/openclaw-gateway.service` a `~/.config/systemd/user/`, revisar rutas de `node` y `openclaw/dist/index.js`, luego `systemctl --user daemon-reload`, `enable --now openclaw-gateway`. Puerto por defecto **18789** (loopback).
6. **Agent Town:** `cd agent-town && pnpm install && pnpm dev` → UI en **http://localhost:3000** (proxy al gateway `ws://127.0.0.1:18789/`).

Perfil CDP del navegador en el repo: `openclaw-state/browser/openclaw/user-data` → enlace a `~/.openclaw/cdp-user-data` (evita rutas de otro usuario).

## Sincronizar desde el equipo (referencia)

Tras cambios locales, desde `~/clawvis-openclaw`: `git add -A`, `git commit`, `git push origin main`.
