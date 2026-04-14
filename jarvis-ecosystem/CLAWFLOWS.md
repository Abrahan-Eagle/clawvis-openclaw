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

## Registro completo de rutinas (con Goal)

Cada rutina debe servir a un goal definido en [GOALS.md](GOALS.md).

### Rutinas propias del ecosistema

| Rutina | Trigger (cron) | Owner | Goal | Archivo canonico |
|--------|---------------|-------|------|------------------|
| Morning Briefing | `30 7 * * *` (7:30 AM UTC diario) | jarvis | G-J01 | `automations/jarvis/morning-briefing.yaml` |
| Competitor Monitor | `0 9 * * 1-5` (9 AM UTC L-V) | marketing | G-M01 | `automations/marketing/competitor-monitor.yaml` |
| Pipeline Report | `0 17 * * 5` (5 PM UTC viernes) | ventas | G-V02 | `automations/ventas/pipeline-report.yaml` |
| Security Audit | `0 8 * * 0` (8 AM UTC domingo) | shared | G-H01 | `automations/shared/security-audit.yaml` |

### Rutinas del registry (instaladas)

| Rutina | Trigger | Descripcion | Skills requeridos |
|--------|---------|-------------|-------------------|
| morning-brief | `30 7 * * *` | Briefing con calendario + clima + TTS | calendar, weather, tts |
| lead-qualifier | (sin trigger) | Scoring de emails/leads | curl, jq |
| rss-digest | `0 8 * * *` | Digest RSS diario | http |
| changelog-monitor | `0 10 * * *` | Monitoreo de releases GitHub | http, storage |
| github-stale-prs | `0 9 * * 1-5` | PRs abiertos sin movimiento | github, notifications |
| github-trending | `0 10 * * *` | Repos trending de GitHub | http |
| weather-commute | `0 7 * * 1-5` | Clima para commute | weather |

### Heartbeats (no son ClawFlows, pero son automatizaciones)

| Agente | Intervalo | Goal | Config |
|--------|-----------|------|--------|
| jarvis | 30 min | G-J01, G-J02 | `openclaw.json` + `agents/jarvis/HEARTBEAT.md` |
| sales-hunter | 1 hora | G-V01 | `openclaw.json` + `agents/ventas/HEARTBEAT.md` |
| mkt-content | 2 horas | G-M01, G-M02 | `openclaw.json` + `agents/marketing/HEARTBEAT.md` |

Detalle operativo de heartbeats: [docs/HEARTBEAT_OPERATIVO.md](docs/HEARTBEAT_OPERATIVO.md).

### Nota sobre duplicados en raiz de automations/

Los archivos `jarvis-morning-briefing.yaml`, `marketing-competitor-monitor.yaml`, `ventas-pipeline-report.yaml`, `shared-security-audit.yaml` en la raiz de `automations/` son copias identicas de los archivos canonicos en subcarpetas. Existen porque `clawflows list` solo lee YAML directamente bajo `CLAWFLOWS_DIR`. **Editar siempre en la subcarpeta y copiar a raiz** (ver `automations/README.md`).

## Recursos comunidad (skills y repos externos)

Inventario curado con criterios de adopcion (no confundir con integraciones ya configuradas en el gateway): [docs/RECURSOS_COMUNIDAD_OPENCLAW.md](docs/RECURSOS_COMUNIDAD_OPENCLAW.md#marketing-openclaw-forense) (ancla al §2 marketing; el documento completo incluye el resto del catalogo).

## Nota

Documentacion adicional del monorepo: [README.md](../README.md) (raiz de `clawvis-openclaw`).
