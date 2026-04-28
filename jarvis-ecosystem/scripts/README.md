# Scripts auxiliares (`jarvis-ecosystem/scripts`)

Todos los paths se asumen desde la raíz **`jarvis-ecosystem/`** (salvo que se indique `source`).

## Shell (bash)

| Script | Propósito | Invocación típica |
|--------|-----------|---------------------|
| [`clawflows-env.sh`](clawflows-env.sh) | Exporta `CLAWFLOWS_DIR`, `CLAWFLOWS_REGISTRY`, `CLAWFLOWS_SKILLS` vía `npm root -g` (sin acoplar a una versión fija de Node). | `source scripts/clawflows-env.sh` |
| [`clawflows-verify-registry.sh`](clawflows-verify-registry.sh) | Ejecuta `clawflows check` sobre cada YAML en `automations/registry/` (requiere CLI `clawflows` + capability map). | `./scripts/clawflows-verify-registry.sh` |
| [`sync-automations-yaml.sh`](sync-automations-yaml.sh) | Copia automations desde subcarpetas (`jarvis/`, `marketing/`, …) a los YAML homónimos en la **raíz** de `automations/` (para `clawflows list`). `--check` solo detecta drift. | `./scripts/sync-automations-yaml.sh` o `./scripts/sync-automations-yaml.sh --check` |
| [`sync-jarvis-skills-from-repo.sh`](sync-jarvis-skills-from-repo.sh) | Sincroniza skills del clon hacia el workspace de Jarvis en el host (`JARVIS_WORKSPACE_BASE`). | Ver [docs/COHERENCIA_RUNTIME_REPO.md](../docs/COHERENCIA_RUNTIME_REPO.md) |
| [`sync-marketing-skills-from-repo.sh`](sync-marketing-skills-from-repo.sh) | Igual para `agents/marketing/skills/` (skills marketing profundas). | `JARVIS_WORKSPACE_BASE=... ./scripts/sync-marketing-skills-from-repo.sh` |
| [`validate-marketing-skills.sh`](validate-marketing-skills.sh) | Wrapper: valida las marketing skills (frontmatter, atribución, enlaces). | `./scripts/validate-marketing-skills.sh` |
| [`smoke-marketing-skills-e2e.sh`](smoke-marketing-skills-e2e.sh) | Smoke end-to-end de marketing skills (requiere entorno/OpenClaw según doc del script). | `./scripts/smoke-marketing-skills-e2e.sh` |
| [`composio-diagnose.sh`](composio-diagnose.sh) | Diagnóstico de red TLS/DNS hacia Composio MCP (no sustituye `openclaw composio doctor`). | `./scripts/composio-diagnose.sh` |
| [`cost-report.sh`](cost-report.sh) | Reporte de uso/coste por agente parseando sesiones JSONL bajo `~/.openclaw/agents/`. | `./scripts/cost-report.sh` o `./scripts/cost-report.sh 2026-04` |
| [`graphify-serve-local.sh`](graphify-serve-local.sh) | Sirve `graphify-out/graph.html` en localhost (127.0.0.1), evita 404 de favicon. Requiere `graphify update` previo en el repo. | `./scripts/graphify-serve-local.sh` |
| [`openclaw-path.sh`](openclaw-path.sh) | Añade al PATH el `openclaw` instalado vía nvm (shells no interactivos / CI). | `source scripts/openclaw-path.sh` |
| [`trello-bootstrap-boards.sh`](trello-bootstrap-boards.sh) | Crea tableros Trello esqueleto (marketing/ventas) — requiere token con escritura. | Ver [docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) |

## Python (marketing skills / generación)

| Ruta | Propósito |
|------|-----------|
| [`validate_marketing_skills.py`](validate_marketing_skills.py) | Validador principal invocado por `validate-marketing-skills.sh`. |
| [`generate_marketing_skills.py`](generate_marketing_skills.py) | Generación/regeneración de skills marketing (legacy/adhoc). |
| [`marketing_skills_v2/`](marketing_skills_v2/) | Paquete v2 (`coordination.py`, `generate.py`, plantillas YAML en `marketing_skills_data/`). |

## Datos YAML (`marketing_skills_data/`)

Definiciones por skill usadas por el generador v2 (coordination, manifests). No se ejecutan solas.

## Ver también

- ClawFlows: [../CLAWFLOWS.md](../CLAWFLOWS.md), [../automations/README.md](../automations/README.md)
- Coherencia repo vs runtime: [../docs/COHERENCIA_RUNTIME_REPO.md](../docs/COHERENCIA_RUNTIME_REPO.md)
- Graphify: [../docs/GRAPHIFY_INTEGRACION.md](../docs/GRAPHIFY_INTEGRACION.md)
