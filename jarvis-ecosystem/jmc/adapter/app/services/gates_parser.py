"""Parsea AG-01..AG-13 desde docs/APPROVAL_GATES.md."""

from __future__ import annotations

import re
from pathlib import Path

from app.services.paths import docs_dir
from app.services.read_capped import read_capped_text

_MD_MAX = 2 * 1024 * 1024


def parse_approval_gates(md_path: Path | None = None) -> list[dict[str, str]]:
    path = md_path or (docs_dir() / "APPROVAL_GATES.md")
    if not path.is_file():
        return []

    text = read_capped_text(path, max_bytes=_MD_MAX)
    if text is None:
        return []
    gates: list[dict[str, str]] = []
    id_re = re.compile(r"`(AG-\d+)`")

    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or "`AG-" not in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 5:
            continue
        # Cabecera de tabla: primera celda "ID" (no confundir con "Acciones" en AG-10).
        if parts[0].strip().upper() == "ID":
            continue
        m = id_re.search(parts[0])
        if not m:
            continue
        gid = m.group(1)
        gates.append(
            {
                "id": gid,
                "action": parts[1],
                "agents": parts[2],
                "level": parts[3],
                "how_to_request": parts[4],
            }
        )
    return gates
