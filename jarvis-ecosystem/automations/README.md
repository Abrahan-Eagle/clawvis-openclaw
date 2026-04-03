# Automatizaciones ClawFlows (Jarvis)

## Directorios

| Ruta | Contenido |
|------|-------------|
| `registry/` | YAML instalados con `clawflows install …` (desde [clawflows.com](https://clawflows.com)) |
| `jarvis/`, `marketing/`, `ventas/`, `shared/`, `devops/` | Flujos propios del ecosistema |

## `clawflows list` vs `registry/`

El CLI solo lista archivos `*.yaml` **directamente** bajo `CLAWFLOWS_DIR`, no en subcarpetas.

- Los flujos custom en la raíz están como **symlinks** (`jarvis-morning-briefing.yaml`, etc.) para que aparezcan en `clawflows list`.
- Para ejecutar algo en `registry/`:

```bash
source /home/will/jarvis-ecosystem/scripts/clawflows-env.sh
clawflows run morning-brief --dir "$CLAWFLOWS_DIR/registry" --dry-run
```

## Variables

Definidas en [`.env`](../.env); para rutas de skills estables ante cambios de versión de Node, preferir:

```bash
source /home/will/jarvis-ecosystem/scripts/clawflows-env.sh
```

Ver [CLAWFLOWS.md](../CLAWFLOWS.md).

## Verificar requisitos del registry

```bash
/home/will/jarvis-ecosystem/scripts/clawflows-verify-registry.sh
/home/will/jarvis-ecosystem/scripts/validate-lead-qualifier-local.sh
```

El mapa de capabilities para el CLI esta en [`agents/jarvis/skills/clawflows-capability-map/CAPABILITY.md`](../agents/jarvis/skills/clawflows-capability-map/CAPABILITY.md).
