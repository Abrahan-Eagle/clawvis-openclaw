"""Rutas /v1/openclaw/*."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.security import require_token
from app.services.cron_timeline import build_cron_timeline
from app.services.openclaw_loader import (
    load_agent_heartbeats,
    load_automations_bundle,
    load_gateway_runtime,
    load_openclaw_agents,
    load_skills_map,
)
from app.util_response import envelope

router = APIRouter(prefix="/openclaw", dependencies=[Depends(require_token)])


@router.get("/agents")
def get_agents():
    return envelope(load_openclaw_agents())


@router.get("/skills")
def get_skills():
    return envelope(load_skills_map())


@router.get("/automations")
def get_automations():
    return envelope(load_automations_bundle())


@router.get("/heartbeats")
def get_heartbeats():
    return envelope(load_agent_heartbeats())


@router.get("/gateway")
def get_gateway(window_hours: int = Query(24, ge=1, le=168)):
    return envelope(load_gateway_runtime(window_hours=window_hours))


@router.get("/cron-timeline")
def get_cron_timeline(days: int = Query(7, ge=1, le=14)):
    return envelope(build_cron_timeline(days=days))
