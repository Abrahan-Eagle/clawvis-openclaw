#!/usr/bin/env python3
"""
Genera `agents/marketing/skills/<name>/SKILL.md` (adaptación v2, español + upstream en references/).

Requisito opcional: clone upstream en `/tmp/marketingskills-upstream/skills/` para versiones y `upstream-en.md`.

Uso (desde `jarvis-ecosystem/scripts/`):

    PYTHONPATH=. python3 -m marketing_skills_v2.generate
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from marketing_skills_v2.generate import main  # noqa: E402


if __name__ == "__main__":
    main()
