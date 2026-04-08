# Automatizaciones ClawFlows (Jarvis)

## Directorios

| Ruta | Contenido |
|------|-----------|
| `registry/` | YAML instalados con `clawflows install …` (desde [clawflows.com](https://clawflows.com)) |
| `jarvis/`, `marketing/`, `ventas/`, `shared/` | Flujos propios del ecosistema |
| `devops/` | (no existe aún en el repo; crear cuando haya flujos DevOps propios) |

## Fuente canónica vs raíz de `automations/`

El CLI solo lista archivos `*.yaml` **directamente** bajo `CLAWFLOWS_DIR`, no en subcarpetas.

- En la **raíz** de `automations/` hay **archivos YAML** con el mismo contenido que los de `jarvis/`, `marketing/`, etc. (para que `clawflows list` los vea). **Edita primero** en `automations/jarvis/`, `automations/marketing/`, `automations/ventas/` — o un solo sitio que el equipo elija — y **vuelve a alinear** la copia de la raíz si cambia el flujo (por ejemplo `diff`/`cp` entre `jarvis/morning-briefing.yaml` y `jarvis-morning-briefing.yaml`).
- **No** asumir symlinks: en este repo las copias en raíz son ficheros regulares idénticos a la última sincronización.

## `clawflows list` vs `registry/`

- Los flujos custom en la raíz existen para el listado del CLI (véase arriba).
- Para ejecutar algo en `registry/`:

```bash
cd "$(git rev-parse --show-toplevel)/jarvis-ecosystem" 2>/dev/null || cd ../..
source scripts/clawflows-env.sh
clawflows run morning-brief --dir "$CLAWFLOWS_DIR/registry" --dry-run
```

(Desde `automations/`, `source ../scripts/clawflows-env.sh` también sirve.)

## Variables

Definidas en [`.env`](../.env); para rutas de skills estables ante cambios de versión de Node, preferir:

```bash
cd "$(git rev-parse --show-toplevel)/jarvis-ecosystem"
source scripts/clawflows-env.sh
```

Ver [CLAWFLOWS.md](../CLAWFLOWS.md).

## Verificar requisitos del registry

Desde el directorio `jarvis-ecosystem/`:

```bash
./scripts/clawflows-verify-registry.sh
./scripts/validate-lead-qualifier-local.sh
```

El mapa de capabilities para el CLI está en [`agents/jarvis/skills/clawflows-capability-map/CAPABILITY.md`](../agents/jarvis/skills/clawflows-capability-map/CAPABILITY.md).
