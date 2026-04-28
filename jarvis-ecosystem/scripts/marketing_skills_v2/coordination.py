"""Bloques de coordinación por categoría (activity-log + handoff)."""
from __future__ import annotations

from typing import TypedDict


class CoordParams(TypedDict, total=False):
    agent_start: str
    agent_target: str
    ref_kind: str
    schema: str


# Categorías alineadas al plan (CRO, Copy, SEO, Paid, Measurement, Retention, Growth, Strategy, Sales, Research)
COORD_BY_CATEGORY: dict[str, CoordParams] = {
    "foundation": {
        "agent_start": "marketing",
        "agent_target": "mkt-content",
        "ref_kind": "marketing-context",
        "schema": "research-to-strategy",
    },
    "cro": {
        "agent_start": "mkt-content",
        "agent_target": "mkt-social",
        "ref_kind": "cro",
        "schema": "strategy-to-copy",
    },
    "copy": {
        "agent_start": "mkt-content",
        "agent_target": "mkt-social",
        "ref_kind": "copy",
        "schema": "copy-to-design",
    },
    "seo": {
        "agent_start": "mkt-seo",
        "agent_target": "mkt-content",
        "ref_kind": "seo",
        "schema": "research-to-strategy",
    },
    "paid": {
        "agent_start": "mkt-paid",
        "agent_target": "mkt-content",
        "ref_kind": "paid-ads",
        "schema": "strategy-to-copy",
    },
    "meas": {
        "agent_start": "mkt-analytics",
        "agent_target": "mkt-content",
        "ref_kind": "analytics",
        "schema": "research-to-strategy",
    },
    "retention": {
        "agent_start": "mkt-content",
        "agent_target": "mkt-social",
        "ref_kind": "retention",
        "schema": "strategy-to-copy",
    },
    "growth": {
        "agent_start": "mkt-growth",
        "agent_target": "mkt-content",
        "ref_kind": "growth",
        "schema": "research-to-strategy",
    },
    "strategy": {
        "agent_start": "mkt-strategy",
        "agent_target": "mkt-content",
        "ref_kind": "strategy",
        "schema": "research-to-strategy",
    },
    "sales": {
        "agent_start": "sales-hunter",
        "agent_target": "sales-closer",
        "ref_kind": "sales-enablement",
        "schema": "research-to-strategy",
    },
    "research": {
        "agent_start": "mkt-research",
        "agent_target": "mkt-strategy",
        "ref_kind": "customer-research",
        "schema": "research-to-strategy",
    },
    "pipeline": {
        "agent_start": "mkt-social",
        "agent_target": "design",
        "ref_kind": "creative-pipeline",
        "schema": "design-to-producer",
    },
}


def render_coordination(category: str) -> str:
    p = COORD_BY_CATEGORY.get(category, COORD_BY_CATEGORY["strategy"])
    agent_start = p.get("agent_start", "mkt-content")
    agent_target = p.get("agent_target", "mkt-social")
    ref_kind = p.get("ref_kind", "marketing")
    schema = p.get("schema", "research-to-strategy")
    return f"""## Coordinación (comandos reales)

Ejecutar desde la raíz del repo `jarvis-ecosystem/` (ajusta rutas si tu cwd es otro).

**1) Iniciar tarea**

```bash
bash skills/global/activity-log/bin/activity-log start \\
  --agent {agent_start} \\
  --title \"Brief / entrega skill\" \\
  --dossier <DOSSIER_ID> \\
  --ref {ref_kind}
```

**2) Registrar hito / artefacto**

```bash
bash skills/global/activity-log/bin/activity-log event \\
  --task <TASK_ID> \\
  --agent {agent_start} \\
  --kind milestone \\
  --note \"Descripción breve del entregable\"
```

**3) Handoff al siguiente rol**

```bash
bash skills/global/handoff/bin/handoff create \\
  --from {agent_start} \\
  --to {agent_target} \\
  --schema {schema} \\
  --task <TASK_ID> \\
  --payload-file /tmp/handoff-payload.json
```

**4) Cerrar**

```bash
bash skills/global/activity-log/bin/activity-log end \\
  --task <TASK_ID> \\
  --note \"Listo para revisión CEO/cliente\"
```

Lista de schemas: `bash skills/global/handoff/bin/handoff schemas`.
"""
