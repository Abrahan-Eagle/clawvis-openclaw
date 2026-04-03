# ClawFlows + Lobster en el ecosistema Jarvis

## Que es

- **[ClawFlows](https://clawflows.com)**: registro de automatizaciones multi-skill para agentes OpenClaw.
- **Lobster**: motor de pipelines deterministas (OpenClaw lo expone como herramienta `lobster` cuando esta en `tools.alsoAllow`).
- **CLI `clawflows`** (`npm i -g clawflows`): buscar, instalar y ejecutar automatizaciones del registry.

## Variables de entorno

En `.env` hay `CLAWFLOWS_DIR` y `CLAWFLOWS_REGISTRY`. Para **`CLAWFLOWS_SKILLS`** (skills empaquetados de OpenClaw + carpeta Jarvis), no uses rutas fijas a `~/.nvm/.../node_modules`: cambian al actualizar Node.

**Recomendado** antes de usar el CLI:

```bash
source /home/will/jarvis-ecosystem/scripts/clawflows-env.sh
```

Ese script define `CLAWFLOWS_SKILLS` con `$(npm root -g)/openclaw/skills` y `agents/jarvis/skills`.

Si solo haces `export $(grep -v '^#' .env | xargs)`, `clawflows check` puede no ver capabilities de skills empaquetados.

## Estructura

```
automations/
  registry/          # YAML instalados desde clawflows.com (clawflows install …)
  jarvis/            # Flujos propios del agente Jarvis
  marketing/
  ventas/
  devops/
  shared/
```

En la raiz de `automations/` hay symlinks a los YAML custom para que `clawflows list` los liste.

## Comandos utiles

```bash
source /home/will/jarvis-ecosystem/scripts/clawflows-env.sh
# opcional: exportar tambien OLLAMA_* desde .env
set -a; source /home/will/jarvis-ecosystem/.env; set +a
clawflows search "query"
clawflows install <nombre> --skip-check   # si faltan capabilities aun
clawflows list
clawflows run jarvis-morning-briefing --dry-run
# Instalaciones bajo automations/registry/:
clawflows run morning-brief --dir "$CLAWFLOWS_DIR/registry" --dry-run
```

Ver `automations/README.md` para la diferencia entre `list` y la carpeta `registry/`.

## Skills instalados (ClawHub) — carpeta compartida

`agents/marketing/skills` y `agents/ventas/skills` apuntan a `agents/jarvis/skills`.

Instalados: `gog`, `himalaya`, `xurl`, `slack`, `blogwatcher`, `summarize`, `notion`, `trello`, `session-logs`, `nano-pdf`, `mcporter`, `tmux`, `video-frames`.

El **CLI ClawHub** global: `npm i -g clawhub` (el skill `clawhub` no existe en el hub; usar el binario `clawhub`).

## Extension global

- `@openclaw/lobster` — plugin de OpenClaw (no hay binario `lobster` suelto; el gateway usa la herramienta).

## Verificacion de automatizaciones del registry

Tras `source scripts/clawflows-env.sh`:

```bash
./scripts/clawflows-verify-registry.sh
./scripts/validate-lead-qualifier-local.sh
```

El directorio `agents/jarvis/skills/clawflows-capability-map/` solo declara **Provides** para que `clawflows check` encuentre capabilities; la ejecucion real sigue dependiendo de los skills y credenciales configurados.

`lead-qualifier` no tiene `metadata.json` en el registry web (`404`), por eso `clawflows check lead-qualifier` falla siempre; el script de verificacion lo omite y el script `validate-lead-qualifier-local.sh` comprueba `curl`/`jq`.

## Nota

En Node 22, `clawflows --version` puede fallar con el paquete npm sin parche (import JSON). Si ocurre, el binario global suele estar en `$(npm root -g)/clawflows/bin/clawflows.mjs`: reemplaza la lectura de `package.json` por `readFileSync` + `JSON.parse` (como en el arreglo ya aplicado en esta maquina), o usa Node 20 LTS para el CLI.
