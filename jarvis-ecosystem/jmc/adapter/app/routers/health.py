"""GET /v1/health."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as pkg_version

from fastapi import APIRouter, Depends

from app.config import BUILD_TIME, get_brand
from app.security import require_token
from app.services.health_deep_builder import build_health_deep
from app.util_response import envelope

router = APIRouter()

try:
    _VER = pkg_version("jmc-adapter")
except PackageNotFoundError:
    _VER = "1.0.0"


@router.get("/health")
def health(_: None = Depends(require_token)):
    return envelope({"status": "ok", "version": _VER, "build_time": BUILD_TIME, "brand": get_brand()})


@router.get("/health/deep")
def health_deep(_: None = Depends(require_token)):
    return envelope(build_health_deep())
