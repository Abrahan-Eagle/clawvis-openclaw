"""Coherencia docs: AG en APPROVAL_GATES vs matriz AUTONOMIA_MODOS."""

from __future__ import annotations

from typing import Any

from app.services.gates_parser import parse_approval_gates
from app.services.modes_resolver import parse_ag_modo_matrix


def run_docs_lints() -> dict[str, Any]:
    gates = parse_approval_gates()
    gate_ids = sorted({g["id"] for g in gates if g.get("id")})
    matrix, mw = parse_ag_modo_matrix()
    matrix_ids = sorted({r.get("gate_id", "") for r in matrix if r.get("gate_id")})

    in_gates_not_matrix = sorted(set(gate_ids) - set(matrix_ids))
    in_matrix_not_gates = sorted(set(matrix_ids) - set(gate_ids))

    return {
        "gates_count": len(gate_ids),
        "matrix_rows": len(matrix_ids),
        "in_gates_not_matrix": in_gates_not_matrix,
        "in_matrix_not_gates": in_matrix_not_gates,
        "ok": not in_gates_not_matrix and not in_matrix_not_gates,
        "warnings": mw,
    }
