"""GET /v1/system/metrics — métricas locales (psutil)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.system_metrics import get_system_metrics
from app.services.system_metrics_extra import get_cpu_detail, get_fs_latency, get_proc_summary
from app.util_response import envelope

router = APIRouter(prefix="/system", dependencies=[Depends(require_token)])


@router.get("/metrics")
def system_metrics():
    return envelope(get_system_metrics())


@router.get("/cpu-detail")
def system_cpu_detail():
    return envelope(get_cpu_detail())


@router.get("/proc-summary")
def system_proc_summary():
    return envelope(get_proc_summary())


@router.get("/fs-latency")
def system_fs_latency():
    return envelope(get_fs_latency())
