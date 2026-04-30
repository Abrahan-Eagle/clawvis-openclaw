"""Rutas /v1/state/*."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from app.config import get_task_zombie_hours
from app.security import require_token
from app.services.activity_insights import compute_agents_stats, compute_latency, compute_zombies
from app.services.jsonl_reader import events_for_dossier, events_for_task, read_activity_tail
from app.services.paths import activity_log_path
from app.services.state_store import (
    aggregate_by_dossier,
    aggregate_tag_counts,
    compute_state_summary,
    handoffs_for_task_id,
    load_handoffs,
    load_pending_approval_handoffs,
    load_task_by_id,
    load_tasks,
)
from app.util_response import envelope

router = APIRouter(prefix="/state", dependencies=[Depends(require_token)])


@router.get("/summary")
def state_summary():
    return envelope(compute_state_summary())


@router.get("/tag-stats")
def state_tag_stats():
    """Conteos por tag (misma lógica que `tag_counts` en /summary)."""
    tasks = load_tasks()
    counts = aggregate_tag_counts(tasks)
    return envelope({"tag_counts": counts, "unique_tags": len(counts)})


@router.get("/pending_approvals")
def state_pending_approvals():
    return envelope({"items": load_pending_approval_handoffs()})


@router.get("/dossier/{dossier_id}")
def state_dossier_detail(dossier_id: str):
    data = aggregate_by_dossier(dossier_id, events_for_dossier)
    warns: list[str] = []
    if (data.get("metrics") or {}).get("events_truncated"):
        warns.append("Lista de eventos del dossier truncada (límite en activity-log).")
    return envelope(data, warnings=warns or None)


@router.get("/tasks/{task_id}")
def state_task_detail(task_id: str):
    task = load_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"error": {"code": "not_found", "message": "Tarea no encontrada"}})
    log = activity_log_path()
    evs, ev_trunc = events_for_task(log, task_id)
    ho = handoffs_for_task_id(task_id)
    warns: list[str] = []
    if ev_trunc:
        warns.append("Lista de eventos truncada (límite de entradas en activity-log).")
    return envelope({"task": task, "events": evs, "handoffs": ho}, warnings=warns or None)


@router.get("/tasks")
def state_tasks():
    return envelope({"tasks": load_tasks()})


@router.get("/handoffs")
def state_handoffs():
    return envelope({"handoffs": load_handoffs()})


@router.get("/activity")
def state_activity(
    limit: int = Query(50, ge=1, le=500),
    cursor: str | None = None,
    since: str | None = Query(None, alias="since"),
    agent: str | None = None,
    kind: str | None = Query(None, description="Filtra campo type del evento"),
):
    data = read_activity_tail(
        activity_log_path(),
        limit=limit,
        cursor=cursor,
        since_iso=since,
        agent=agent,
        event_type=kind,
    )
    return envelope(data)


@router.get("/agents-stats")
def state_agents_stats():
    return envelope(compute_agents_stats(activity_log_path()))


@router.get("/zombies")
def state_zombies(hours: float | None = Query(None, ge=1.0, le=720.0)):
    h = float(hours) if hours is not None else get_task_zombie_hours()
    return envelope(compute_zombies(activity_log_path(), h))


@router.get("/latency")
def state_latency():
    return envelope(compute_latency(activity_log_path()))
