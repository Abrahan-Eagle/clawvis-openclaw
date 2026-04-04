# Ecosistema Jarvis (dentro de `clawvis-openclaw`)

Este directorio agrupa **agentes**, **skills**, **automatizaciones ClawFlows** y **scripts** para OpenClaw. La documentación operativa global está en el [README.md del monorepo](../README.md).

## Tres sitios distintos: no confundir

| Ubicación | Rol |
|-----------|-----|
| **`jarvis-ecosystem/openclaw.json`** (este árbol) | **Plantilla / referencia** mínima (modelos de ejemplo, bindings de ejemplo). El gateway **no** la lee salvo que la copies a mano. |
| **`~/.openclaw/openclaw.json`** | **Fuente de verdad** del gateway: modelos reales, canales (Telegram, Discord, WhatsApp), `bindings`, `tools`, agentes. Editar aquí para cambiar comportamiento en producción. |
| **`config/openclaw-home/`** (en el monorepo) | **Instantánea sanitizada** (sin `.env`, sin sesiones ni credenciales) para revisión y backup en Git. Aproxima tu `~/.openclaw` pero no sustituye el archivo vivo. |

## Contenido principal

| Ruta | Descripción |
|------|-------------|
| `agents/jarvis/` | Workspace principal: `AGENTS.md`, `SOUL.md`, `skills/`, `scripts/` (model-router), `memory/`. |
| `agents/marketing/`, `agents/ventas/` | Perfiles de agente; las carpetas `skills/` repiten el contenido de `agents/jarvis/skills` (copias por skill). **Canónico para editar skills:** `agents/jarvis/skills/`. |
| `automations/` | YAML ClawFlows; ver [automations/README.md](automations/README.md) (raíz vs subcarpetas). |
| `scripts/` | `clawflows-env.sh`, verificación del registry, etc. |
| [CLAWFLOWS.md](CLAWFLOWS.md) | Guía ClawFlows + Lobster. |

## Checklist rápido

- Cambiar **Telegram / modelo / binding** → `~/.openclaw/openclaw.json` + reinicio del gateway.
- Cambiar **skill o prompt del agente** → `agents/jarvis/skills/` (y alinear copias en marketing/ventas si las usas).
- **Backup de config en Git** → actualizar `config/openclaw-home/` según el procedimiento del README raíz (sin secretos).
