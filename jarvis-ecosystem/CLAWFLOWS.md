# ClawFlows + Lobster en el ecosistema Jarvis

## Prompt core, memoria y skills del repo (2026-04)

- **Protocolo compartido (texto, no voz):** [skills/global/core-prompt.md](skills/global/core-prompt.md). Cada `agents/*/SOUL.md` hereda con una línea al inicio; cámbialo una sola vez aquí para alinear routing y approval gates.
- **Memoria operativa por agente:** [skills/global/memory-store/](skills/global/memory-store/) + `agents/<agente>/memory.json` (Session Startup: `format-prompt`); `MEMORY.md` = prosa. Consolidación HITL: `scripts/memory-consolidate.sh`. Compactación: [session-compact-ops](skills/global/session-compact-ops/SKILL.md). Judge pre-AG-12: [judge-run](skills/global/judge-run/SKILL.md) → `state/judge/`. Lecciones: `scripts/lessons-scan.sh`. Context packs: [contexts/](contexts/).
- **Skills añadidos en este ecosistema** (además de ClawHub): `weather-report`, `youtube-transcript`, `browser-playwright`, conjunto `planner` / `task-queue` / `executor` / `error-recovery` (ver `automations/jarvis/loop-orchestrator.yaml`), y el bloque **v2 abril 2026**: skills globales `activity-log`, `handoff`, `coordinator` (coordinacion); pipeline RRSS local `brand-kit`, `image-render`, `image-ai-free`, `carousel-render`, `tts-free`, `subtitles`, `video-compose`, `video-short` (esqueleto). Ver [docs/PROPUESTA_MEJORA_JARVIS_V2.md](docs/PROPUESTA_MEJORA_JARVIS_V2.md), [docs/COORDINACION_AGENTES.md](docs/COORDINACION_AGENTES.md), [docs/CAROUSEL_PIPELINE_FREE.md](docs/CAROUSEL_PIPELINE_FREE.md), [docs/REELS_TIKTOK_PIPELINE_FREE.md](docs/REELS_TIKTOK_PIPELINE_FREE.md).

El **runtime OpenClaw** no carga automáticamente `core-prompt.md` en el system prompt: el agente (o tú) debe **leerlo al inicio de sesión** o enlazarlo en la configuración del gateway si tu versión soporta inyección. Hasta entonces, la línea *Hereda* en `SOUL.md` es el recordatorio de convenio del equipo.

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

**Skills por capa (jul 2026):**

- `agents/jarvis/skills/` — skills globales JARVIS + ClawHub + variantes `*-ops` (canónico para ops de gobierno).
- `agents/marketing/skills/` — **40 skills de dominio** (marketingskills / guías v2). **No** son copia de jarvis; son exclusivas de marketing.
- `agents/ventas/skills/career-ops/` — solo Ventas.
- `skills/` y `skills/global/` — CLIs de producción y coordinación (carousel-render, handoff, editorial-calendar, approval-gate, mkt-publish, …). Ver [docs/MANUAL_RRSS_JARVIS.md](docs/MANUAL_RRSS_JARVIS.md).

Instalados: `gog`, `himalaya`, `xurl`, `slack`, `blogwatcher`, `summarize`, `notion`, `trello`, `session-logs`, `nano-pdf`, `mcporter`, `tmux`, `video-frames`.

El **CLI ClawHub** global: `npm i -g clawhub` (el skill `clawhub` no existe en el hub; usar el binario `clawhub`).

## Extension global

- `@openclaw/lobster` — plugin de OpenClaw (no hay binario `lobster` suelto; el gateway usa la herramienta).

## Verificacion de automatizaciones del registry

Tras `source scripts/clawflows-env.sh` (desde `jarvis-ecosystem/`):

```bash
./scripts/clawflows-verify-registry.sh
```

El directorio `agents/jarvis/skills/clawflows-capability-map/` solo declara **Provides** para que `clawflows check` encuentre capabilities; la ejecucion real sigue dependiendo de los skills y credenciales configurados.

### clawflows + Node 22

En Node 22, `clawflows --version` puede fallar con el paquete npm sin parche (import JSON). Si ocurre, el binario global suele estar en `$(npm root -g)/clawflows/bin/clawflows.mjs`: reemplaza la lectura de `package.json` por `readFileSync` + `JSON.parse` (parche local en esa máquina), o usa **Node 20 LTS** solo para el CLI de ClawFlows. No afecta al gateway OpenClaw si este usa otro Node.

### CLI `openclaw` (PATH en shells no interactivos)

El bin `openclaw` suele instalarse con `npm i -g openclaw` bajo el Node de nvm; en **shells no interactivos** (scripts, CI, pruebas) `nvm` no carga y el comando puede dar *orden no encontrada*. Desde `jarvis-ecosystem/`:

```bash
source scripts/openclaw-path.sh
openclaw --version
```

Opcional: `OPENCLAW_NODE_VERSION=22` (o `20`, etc.) antes del `source` para fijar la versión de Node cuyo `bin/` contiene `openclaw`. Ver [scripts/openclaw-path.sh](scripts/openclaw-path.sh). No sustituye a `clawflows-env.sh` (ese script solo arma `CLAWFLOWS_SKILLS` para el CLI ClawFlows).

## Registro completo de rutinas (con Goal)

Cada rutina debe servir a un goal definido en [GOALS.md](GOALS.md).

### Rutinas propias del ecosistema

| Rutina | Trigger (cron) | Owner | Goal | Archivo canonico |
|--------|---------------|-------|------|------------------|
| Morning Briefing | `30 7 * * *` (7:30 AM UTC diario) | jarvis | G-J01 | `automations/jarvis/morning-briefing.yaml` |
| Coordination Pulse | `0 */4 * * *` (cada 4h) | jarvis | G-J01 | `automations/jarvis/coordination-pulse.yaml` |
| Competitor Monitor | `0 9 * * 1-5` (9 AM UTC L-V) | marketing | G-M01 | `automations/marketing/competitor-monitor.yaml` |
| Content Production Pipeline | `0 */6 * * *` (cada 6h) | marketing | G-M02 | `automations/marketing/content-production-pipeline.yaml` |
| Pipeline Report | `0 17 * * 5` (5 PM UTC viernes) | ventas | G-V02 | `automations/ventas/pipeline-report.yaml` |
| Security Audit | `0 8 * * 0` (8 AM UTC domingo) | shared | G-H01 | `automations/shared/security-audit.yaml` |

### Rutinas del registry (instaladas)

| Rutina | Trigger | Descripcion | Skills requeridos |
|--------|---------|-------------|-------------------|
| morning-brief | `30 7 * * *` | Briefing con calendario + clima + TTS | calendar, weather, tts |
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
