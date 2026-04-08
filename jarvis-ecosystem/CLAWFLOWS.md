# ClawFlows + Lobster en el ecosistema Jarvis

## Que es

- **[ClawFlows](https://clawflows.com)**: registro de automatizaciones multi-skill para agentes OpenClaw.
- **Lobster**: motor de pipelines deterministas (OpenClaw lo expone como herramienta `lobster` cuando está en `tools.alsoAllow`).
- **CLI `clawflows`** (`npm i -g clawflows`): buscar, instalar y ejecutar automatizaciones del registry.

## Variables de entorno

En `.env` hay `CLAWFLOWS_REGISTRY` y opcionalmente `CLAWFLOWS_DIR`. Para **`CLAWFLOWS_SKILLS`** (skills empaquetados de OpenClaw + carpeta Jarvis), no uses rutas fijas a `~/.nvm/.../node_modules`: cambian al actualizar Node.

**Recomendado** antes de usar el CLI (desde el directorio `jarvis-ecosystem` del monorepo, sea cual sea la ruta del clon):

```bash
cd /ruta/a/tu/clon/clawvis-openclaw/jarvis-ecosystem
source scripts/clawflows-env.sh
```

Alternativa portable si estás en la raíz del repo Git:

```bash
cd "$(git rev-parse --show-toplevel)/jarvis-ecosystem"
source scripts/clawflows-env.sh
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

En la raíz de `automations/` hay copias de los YAML custom (mismo contenido que en subcarpetas) para que `clawflows list` los liste; la **fuente canónica** para editar está en `automations/jarvis/`, `marketing/`, `ventas/` (ver `automations/README.md`).

## Comandos utiles

```bash
cd "$(git rev-parse --show-toplevel)/jarvis-ecosystem" 2>/dev/null || cd /ruta/a/jarvis-ecosystem
source scripts/clawflows-env.sh
# opcional: exportar tambien OLLAMA_* desde .env
set -a; source .env; set +a
clawflows search "query"
clawflows install <nombre> --skip-check   # si faltan capabilities aun
clawflows list
clawflows run jarvis-morning-briefing --dry-run
# Instalaciones bajo automations/registry/:
clawflows run morning-brief --dir "$CLAWFLOWS_DIR/registry" --dry-run
```

Ver `automations/README.md` para la diferencia entre `list` y la carpeta `registry/`.

## Skills instalados (ClawHub) — carpeta compartida

`agents/marketing/skills` y la mayor parte de `agents/ventas/skills` duplican el contenido de `agents/jarvis/skills` (copias por skill). **Excepción:** `agents/ventas/skills/career-ops/` es solo Ventas (no existe en jarvis). **Canónico para editar:** `agents/jarvis/skills/`; luego sincronizar o reinstalar según tu flujo (ver `README.md` en la raíz de `jarvis-ecosystem/`).

Instalados: `gog`, `himalaya`, `xurl`, `slack`, `blogwatcher`, `summarize`, `notion`, `trello`, `session-logs`, `nano-pdf`, `mcporter`, `tmux`, `video-frames`.

El **CLI ClawHub** global: `npm i -g clawhub` (el skill `clawhub` no existe en el hub; usar el binario `clawhub`).

## Extension global

- `@openclaw/lobster` — plugin de OpenClaw (no hay binario `lobster` suelto; el gateway usa la herramienta).

## Verificacion de automatizaciones del registry

Tras `source scripts/clawflows-env.sh` (desde `jarvis-ecosystem/`):

```bash
./scripts/clawflows-verify-registry.sh
./scripts/validate-lead-qualifier-local.sh
```

El directorio `agents/jarvis/skills/clawflows-capability-map/` solo declara **Provides** para que `clawflows check` encuentre capabilities; la ejecucion real sigue dependiendo de los skills y credenciales configurados.

### lead-qualifier (registry)

`lead-qualifier` no tiene `metadata.json` en el registry web (**404**), por eso `clawflows check lead-qualifier` falla siempre; el script de verificación lo omite y el script `validate-lead-qualifier-local.sh` comprueba `curl`/`jq`. Revisar cuando el registry publique metadata; hasta entonces no es fallo del ecosistema local.

### clawflows + Node 22

En Node 22, `clawflows --version` puede fallar con el paquete npm sin parche (import JSON). Si ocurre, el binario global suele estar en `$(npm root -g)/clawflows/bin/clawflows.mjs`: reemplaza la lectura de `package.json` por `readFileSync` + `JSON.parse` (parche local en esa máquina), o usa **Node 20 LTS** solo para el CLI de ClawFlows. No afecta al gateway OpenClaw si este usa otro Node.

## Recursos comunidad (skills y repos externos)

Inventario curado con criterios de adopción (no confundir con integraciones ya configuradas en el gateway): [docs/RECURSOS_COMUNIDAD_OPENCLAW.md](docs/RECURSOS_COMUNIDAD_OPENCLAW.md#marketing-openclaw-forense) (ancla al §2 marketing; el documento completo incluye el resto del catálogo).

## Nota

Documentacion adicional del monorepo: [README.md](../README.md) (raíz de `clawvis-openclaw`).
