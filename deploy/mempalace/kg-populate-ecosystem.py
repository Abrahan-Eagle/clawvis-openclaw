#!/usr/bin/env python3
"""
Puebla el Knowledge Graph temporal de MemPalace con hechos del holding Jarvis.
Requiere: pipx install mempalace (mismo entorno que el CLI).

Ejecución típica:
  ~/.local/share/pipx/venvs/mempalace/bin/python3 deploy/mempalace/kg-populate-ecosystem.py

O: export MEMPALACE_PYTHON=.../python3  && ./kg-populate-ecosystem.sh
"""

from __future__ import annotations

import sys

try:
    from mempalace.knowledge_graph import KnowledgeGraph
except ImportError:
    print(
        "No se pudo importar mempalace. Use el Python del venv pipx, p. ej.:\n"
        "  ~/.local/share/pipx/venvs/mempalace/bin/python3 "
        "deploy/mempalace/kg-populate-ecosystem.py",
        file=sys.stderr,
    )
    sys.exit(1)

# Triples: subject, predicate, object, valid_from, valid_to
FACTS: list[tuple[str, str, str, str | None, str | None]] = [
    ("Abrahan Pulido", "role_in", "CEO del holding", "2026-04-04", None),
    ("Jarvis", "role_in", "Agente maestro / orquestador", "2026-04-04", None),
    ("Abrahan Pulido", "owns", "Aiblock", "2026-01-01", None),
    ("Abrahan Pulido", "controls", "Jarvis ecosystem", "2026-04-04", None),
    ("marketing", "is_a", "Empresa activa del holding", "2026-04-04", None),
    ("marketing", "provides", "Marketing digital, redes, branding, contenido, publicidad", "2026-04-04", None),
    ("marketing", "workspace", "agents/marketing/", "2026-04-04", None),
    ("ventas", "is_a", "Empresa activa del holding", "2026-04-04", None),
    ("ventas", "provides", "Prospeccion, cierre, pipeline comercial, Workana", "2026-04-04", None),
    ("ventas", "workspace", "agents/ventas/", "2026-04-04", None),
    ("dev-agency", "is_a", "Empresa planificada del holding", "2026-04-04", None),
    ("legal", "is_a", "Empresa planificada del holding", "2026-04-04", None),
    ("contadores", "is_a", "Empresa planificada del holding", "2026-04-04", None),
    ("jarvis", "agent_of", "holding (master)", "2026-04-04", None),
    ("mkt-content", "agent_of", "marketing", "2026-04-04", None),
    ("mkt-social", "agent_of", "marketing", "2026-04-04", None),
    ("mkt-analytics", "agent_of", "marketing", "2026-04-04", None),
    ("mkt-ads", "agent_of", "marketing", "2026-04-04", None),
    ("mkt-email", "agent_of", "marketing", "2026-04-04", None),
    ("sales-hunter", "agent_of", "ventas", "2026-04-04", None),
    ("sales-closer", "agent_of", "ventas", "2026-04-04", None),
    ("sales-account", "agent_of", "ventas", "2026-04-04", None),
    ("cli-20260404-ejemplo", "client_of", "marketing", "2026-04-04", None),
    ("cli-20260404-cliente-tests-redes", "client_of", "marketing", "2026-04-04", None),
    ("gobierno_v2", "decided_on", "2026-04-04", "2026-04-04", None),
    ("flujo_ventas", "decided_on", "2026-04-08", "2026-04-08", None),
    ("mempalace_integration", "decided_on", "2026-04-08", "2026-04-08", None),
    ("Jarvis ecosystem", "uses", "OpenClaw gateway", "2026-04-04", None),
    ("Jarvis ecosystem", "uses", "Trello (fuente de verdad)", "2026-04-04", None),
    ("Jarvis ecosystem", "uses", "MemPalace (memoria avanzada)", "2026-04-08", None),
]


def main() -> None:
    kg = KnowledgeGraph()
    n = 0
    for subj, pred, obj, vf, vt in FACTS:
        try:
            kg.add_triple(subj, pred, obj, valid_from=vf, valid_to=vt)
            n += 1
        except Exception as e:
            print(f"WARN: {subj} {pred} {obj}: {e}", file=sys.stderr)
    print(f"KG: {n}/{len(FACTS)} triples añadidos (idempotente si ya existían según implementación).")
    print(kg.stats())


if __name__ == "__main__":
    main()
