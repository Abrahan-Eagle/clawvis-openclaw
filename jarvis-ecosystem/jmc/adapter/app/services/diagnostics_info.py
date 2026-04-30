"""GET /v1/diagnostics — sin secretos."""

from __future__ import annotations

import os
import platform
import sys
from importlib.metadata import PackageNotFoundError, version as pkg_version
from typing import Any

from app.config import BUILD_TIME, get_bind, get_port, get_repo_root
from app.services.paths import openclaw_json_path, state_dir


def build_diagnostics() -> dict[str, Any]:
    ver = "1.0.0"
    try:
        ver = pkg_version("jmc-adapter")
    except PackageNotFoundError:
        pass
    return {
        "adapter_version": ver,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "build_time": BUILD_TIME,
        "bind": get_bind(),
        "port": get_port(),
        "repo_root": str(get_repo_root()),
        "state_dir": str(state_dir()),
        "openclaw_json_path": str(openclaw_json_path()),
        "cwd": os.getcwd(),
    }
