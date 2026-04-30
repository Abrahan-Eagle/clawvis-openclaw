"""Tests JMC adapter con repo temporal y fixtures."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

HDR = {"Authorization": "Bearer " + "k" * 32}


@pytest.fixture
def jwt_ok(monkeypatch):
    monkeypatch.setenv("JMC_BEARER_TOKEN", "k" * 32)


def _clear_repo_cache():
    from app.config import get_repo_root

    get_repo_root.cache_clear()


def _seed_repo_base(tmp_path):
    """Repo mínimo compatible con tests existentes."""
    doc = tmp_path / "docs"
    doc.mkdir()
    (doc / "APPROVAL_GATES.md").write_text(
        """
## Tabla de approval gates

| ID | Accion | Agentes afectados | Nivel | Como solicitar |
|----|--------|--------------------|-------|----------------|
| `AG-01` | Test accion | jarvis | CEO | Trello |
""",
        encoding="utf-8",
    )
    (doc / "AUTONOMIA_MODOS.md").write_text(
        """# Modos

## Matriz AG × Modo

| Gate | D | C | B | A |
|------|---|---|---|---|
| AG-01 Demo gate | Siempre CEO | Escala | Solo | Piloto |
""",
        encoding="utf-8",
    )
    (tmp_path / "openclaw.json").write_text(
        json.dumps({"agents": {"list": [{"id": "jarvis", "workspace": "./agents/jarvis"}]}}),
        encoding="utf-8",
    )
    st = tmp_path / "state"
    (st / "tasks").mkdir(parents=True)
    (st / "tasks" / "task-demo.json").write_text(
        json.dumps(
            {
                "id": "task-demo",
                "status": "blocked",
                "owner": "jarvis",
                "started_at": "2026-04-28T10:00:00Z",
                "title": "demo",
            }
        ),
        encoding="utf-8",
    )
    (st / "handoffs").mkdir(exist_ok=True)
    (st / "handoffs" / "ho1.json").write_text(json.dumps({"schema": "h1", "from": "a", "to": "b", "task_id": "task-demo"}))
    (st / "activity-log.jsonl").write_text(
        '{"ts":"2026-04-28T12:00:00Z","agent":"jarvis","type":"start","task_id":"task-demo"}\n',
        encoding="utf-8",
    )
    cd = tmp_path / "client-dossiers"
    cd.mkdir()
    (cd / "cli-test.json").write_text(json.dumps({"client": "X", "consumerKey": "SECRET"}), encoding="utf-8")
    sk = tmp_path / "agents" / "jarvis" / "skills" / "demo-skill"
    sk.mkdir(parents=True)
    (sk / "SKILL.md").write_text("---\nname: demo-skill\ndescription: test\n---\n", encoding="utf-8")
    (tmp_path / "automations").mkdir()
    (tmp_path / "automations" / "x.yaml").write_text("foo: bar\n", encoding="utf-8")
    sc = tmp_path / "scripts"
    sc.mkdir()
    (sc / "sync-automations-yaml.sh").write_text("#!/bin/bash\nexit 0\n", encoding="utf-8")
    (sc / "cost-report.sh").write_text(
        """#!/bin/bash
# Salida mínima parseable por cost_report._parse_cost_report_text
cat <<'EOF'
TOTAL tokens est.: 999

--- jarvis ---
  Sesiones activas: 2
  Mensajes user: 5
  Mensajes assistant: 10
  Tokens IN: 100
  Tokens OUT: 200
  Tokens total: 300
EOF
""",
        encoding="utf-8",
    )


@pytest.fixture
def client_tmp(tmp_path, monkeypatch, jwt_ok):
    monkeypatch.setenv("JMC_REPO_ROOT", str(tmp_path))
    monkeypatch.setenv("JMC_OPENCLAW_JSON_PATH", str(tmp_path / "openclaw.json"))
    _clear_repo_cache()
    _seed_repo_base(tmp_path)
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


@pytest.fixture
def client_v12(tmp_path, monkeypatch, jwt_ok):
    """Repo extendido para endpoints v1.2 (dossier, approvals, summary, heartbeats)."""
    monkeypatch.setenv("JMC_REPO_ROOT", str(tmp_path))
    monkeypatch.setenv("JMC_OPENCLAW_JSON_PATH", str(tmp_path / "openclaw.json"))
    _clear_repo_cache()
    _seed_repo_base(tmp_path)
    st = tmp_path / "state"
    _recent_open = (datetime.now(timezone.utc) - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
    (tmp_path / "openclaw.json").write_text(
        json.dumps(
            {
                "agents": {
                    "list": [
                        {
                            "id": "jarvis",
                            "workspace": "./agents/jarvis",
                            "heartbeat": {
                                "every": "30m",
                                "target": "none",
                                "activeHours": {"start": "08:00", "end": "24:00", "timezone": "UTC"},
                            },
                        }
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    (st / "tasks" / "td-open.json").write_text(
        json.dumps(
            {
                "id": "td-open",
                "status": "in_progress",
                "owner": "jarvis",
                "dossier_id": "d1",
                "started_at": _recent_open,
                "title": "open d1",
                "tags": ["infra", "demo"],
            }
        ),
        encoding="utf-8",
    )
    (st / "tasks" / "td-done.json").write_text(
        json.dumps(
            {
                "id": "td-done",
                "status": "done",
                "owner": "jarvis",
                "dossier_id": "d1",
                "started_at": "2026-04-27T10:00:00Z",
                "title": "done d1",
            }
        ),
        encoding="utf-8",
    )
    (st / "tasks" / "td-stall.json").write_text(
        json.dumps(
            {
                "id": "td-stall",
                "status": "in_progress",
                "owner": "jarvis",
                "started_at": "2020-01-01T10:00:00Z",
                "title": "stalled",
            }
        ),
        encoding="utf-8",
    )
    (st / "handoffs" / "ho-d1.json").write_text(
        json.dumps(
            {
                "id": "ho-d1",
                "schema": "producer-to-publisher",
                "from": "a",
                "to": "b",
                "task_id": "td-open",
                "dossier_id": "d1",
            }
        ),
        encoding="utf-8",
    )
    (st / "handoffs" / "ho-pend.json").write_text(
        json.dumps(
            {
                "id": "ho-pend",
                "schema": "x",
                "task_id": "td-open",
                "payload": {"approval": {"ag": "AG-12", "status": "pending"}, "channels": ["instagram_reels"]},
            }
        ),
        encoding="utf-8",
    )
    (st / "handoffs" / "ho-approved.json").write_text(
        json.dumps(
            {
                "id": "ho-approved",
                "schema": "y",
                "task_id": "task-demo",
                "accepted_at": "2026-04-28T14:00:00Z",
                "payload": {"approval": {"ag": "AG-01", "status": "approved"}},
            }
        ),
        encoding="utf-8",
    )
    (st / "handoffs" / "ho-accepted.json").write_text(
        json.dumps(
            {
                "id": "ho-accepted",
                "schema": "z",
                "task_id": "task-demo",
                "accepted_at": "2026-04-28T13:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    log_extra = (
        '{"ts":"2026-04-28T11:00:00Z","agent":"jarvis","type":"event","dossier_id":"d1","task_id":"td-open"}\n'
        '{"ts":"2026-04-28T11:30:00Z","agent":"jarvis","type":"note","dossier_id":"d1"}\n'
    )
    (st / "activity-log.jsonl").write_text(
        '{"ts":"2026-04-28T12:00:00Z","agent":"jarvis","type":"start","task_id":"task-demo"}\n' + log_extra,
        encoding="utf-8",
    )
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


def test_health_envelope(client_tmp):
    r = client_tmp.get("/v1/health", headers={"Authorization": "Bearer " + "k" * 32})
    assert r.status_code == 200
    body = r.json()
    assert body["meta"]["version"] == "v1"
    assert body["data"]["status"] == "ok"


def test_tasks_and_escalations(client_tmp):
    r = client_tmp.get("/v1/state/tasks", headers={"Authorization": "Bearer " + "k" * 32})
    assert r.status_code == 200
    tasks = r.json()["data"]["tasks"]
    assert len(tasks) == 1
    assert tasks[0]["jmc_status"] == "waiting_for_user"

    r2 = client_tmp.get("/v1/escalations", headers={"Authorization": "Bearer " + "k" * 32})
    assert r2.status_code == 200
    assert len(r2.json()["data"]["items"]) == 1


def test_dossiers_redact(client_tmp):
    r = client_tmp.get("/v1/dossiers", headers={"Authorization": "Bearer " + "k" * 32})
    assert r.status_code == 200
    items = r.json()["data"]["items"]
    cli = next(x for x in items if x.get("id") == "cli-test")
    assert cli["data"]["consumerKey"] == "[redacted]"


def test_unauthorized(client_tmp):
    r = client_tmp.get("/v1/health")
    assert r.status_code == 401
    assert r.json()["detail"]["error"]["code"] == "unauthorized"


def test_auth_wrong_bearer(client_tmp):
    r = client_tmp.get("/v1/health", headers={"Authorization": "Bearer " + "z" * 32})
    assert r.status_code == 401
    assert r.json()["detail"]["error"]["code"] == "unauthorized"


def test_auth_misconfigured_short_token(monkeypatch):
    monkeypatch.setenv("JMC_BEARER_TOKEN", "x" * 8)
    from fastapi.testclient import TestClient

    from app.main import app

    c = TestClient(app)
    r = c.get("/v1/health", headers={"Authorization": "Bearer " + "x" * 8})
    assert r.status_code == 503
    assert r.json()["detail"]["error"]["code"] == "misconfigured"


def test_gates_parsed(client_tmp):
    r = client_tmp.get("/v1/gates", headers={"Authorization": "Bearer " + "k" * 32})
    assert r.status_code == 200
    gates = r.json()["data"]["gates"]
    assert any(g["id"] == "AG-01" for g in gates)


def _clear_cost_cache():
    from app.services import cost_report as cr

    cr._CACHE.clear()
    cr._INFLIGHT.clear()


def test_modes_matrix(client_tmp):
    r = client_tmp.get("/v1/modes/matrix", headers={"Authorization": "Bearer " + "k" * 32})
    assert r.status_code == 200
    rows = r.json()["data"]["matrix"]
    assert len(rows) == 1
    assert rows[0]["gate_id"] == "AG-01"
    assert rows[0]["D"] == "Siempre CEO"


def test_modes_get_capability_flag(client_tmp):
    r = client_tmp.get("/v1/modes/current", headers=HDR)
    assert r.status_code == 200
    assert r.json()["data"].get("mode_write_enabled") is True


def test_modes_post_allowed_without_jmc_allow_env(client_tmp, monkeypatch, tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("JMC_OPENCLAW_ENV_PATH", raising=False)
    monkeypatch.delenv("JARVIS_AUTONOMY_MODE", raising=False)
    r = client_tmp.post("/v1/modes/current", headers=HDR, json={"mode": "C"})
    assert r.status_code == 200
    assert r.json()["data"]["effective_mode"] == "C"
    env_file = home / ".openclaw" / ".env"
    text = env_file.read_text(encoding="utf-8")
    assert "JARVIS_AUTONOMY_MODE=C" in text.replace(" ", "")


def test_modes_post_invalid_mode(client_tmp, monkeypatch):
    r = client_tmp.post("/v1/modes/current", headers=HDR, json={"mode": "Z"})
    assert r.status_code == 400
    assert r.json()["detail"]["error"]["code"] == "invalid_mode"


def test_modes_post_rejects_extra_fields(client_tmp):
    r = client_tmp.post("/v1/modes/current", headers=HDR, json={"mode": "C", "extra": 1})
    assert r.status_code == 422


def test_modes_post_writes_env_file(client_tmp, monkeypatch, tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    env_file = home / ".openclaw" / "test.env"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("JMC_OPENCLAW_ENV_PATH", str(env_file))
    monkeypatch.delenv("JARVIS_AUTONOMY_MODE", raising=False)
    r = client_tmp.post("/v1/modes/current", headers=HDR, json={"mode": "B"})
    assert r.status_code == 200
    assert r.json()["data"]["effective_mode"] == "B"
    text = env_file.read_text(encoding="utf-8")
    assert "JARVIS_AUTONOMY_MODE=B" in text.replace(" ", "")


def test_modes_post_rejects_env_outside_openclaw(client_tmp, monkeypatch, tmp_path):
    bad = tmp_path / "outside.env"
    monkeypatch.setenv("JMC_OPENCLAW_ENV_PATH", str(bad))
    r = client_tmp.post("/v1/modes/current", headers=HDR, json={"mode": "A"})
    assert r.status_code == 400
    assert r.json()["detail"]["error"]["code"] == "invalid_env_path"


def test_state_task_detail_ok_and_404(client_tmp):
    r = client_tmp.get("/v1/state/tasks/task-demo", headers={"Authorization": "Bearer " + "k" * 32})
    assert r.status_code == 200
    body = r.json()["data"]
    assert body["task"]["id"] == "task-demo"
    assert isinstance(body["events"], list)
    assert len(body["events"]) == 1
    assert isinstance(body["handoffs"], list)
    assert any(h.get("task_id") == "task-demo" for h in body["handoffs"])

    r404 = client_tmp.get("/v1/state/tasks/no-existe-xyz", headers={"Authorization": "Bearer " + "k" * 32})
    assert r404.status_code == 404


def test_state_task_rejects_path_traversal_id(client_tmp):
    from urllib.parse import quote

    tid = quote("../../etc/passwd", safe="")
    r = client_tmp.get(f"/v1/state/tasks/{tid}", headers={"Authorization": "Bearer " + "k" * 32})
    assert r.status_code == 404


def test_state_activity_invalid_cursor_ok(client_tmp):
    h = {"Authorization": "Bearer " + "k" * 32}
    r_bad = client_tmp.get("/v1/state/activity?limit=10&cursor=not-an-int", headers=h)
    r0 = client_tmp.get("/v1/state/activity?limit=10&cursor=0", headers=h)
    assert r_bad.status_code == 200 and r0.status_code == 200
    db = r_bad.json()["data"]
    d0 = r0.json()["data"]
    assert db["events"] == d0["events"]
    assert db.get("next_cursor") == d0.get("next_cursor")
    assert db.get("total_filtered") == d0.get("total_filtered")


def test_costs_summary_invalid_month_422(client_tmp):
    r = client_tmp.get("/v1/costs/summary?month=2026-13", headers=HDR)
    assert r.status_code == 422
    assert r.json()["detail"]["error"]["code"] == "invalid_month"


def test_openclaw_agents_skills_automations(client_tmp):
    ra = client_tmp.get("/v1/openclaw/agents", headers=HDR)
    assert ra.status_code == 200
    d = ra.json()["data"]
    assert "source" in d and "agents" in d
    rs = client_tmp.get("/v1/openclaw/skills", headers=HDR)
    assert rs.status_code == 200
    assert "workspaces" in rs.json()["data"]
    rm = client_tmp.get("/v1/openclaw/automations", headers=HDR)
    assert rm.status_code == 200
    mj = rm.json()["data"]
    assert mj.get("root") == "automations"
    assert "sync_check" in mj


def test_state_handoffs_list(client_tmp):
    r = client_tmp.get("/v1/state/handoffs", headers=HDR)
    assert r.status_code == 200
    hands = r.json()["data"]["handoffs"]
    assert isinstance(hands, list)
    assert any(h.get("task_id") == "task-demo" for h in hands)


def test_modes_doc_fragment(client_tmp):
    r = client_tmp.get("/v1/modes/doc_fragment", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "snippet" in d and "path" in d


def test_judge_last_envelope(client_tmp):
    r = client_tmp.get("/v1/judge/last", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "runs" in d


def test_last30days_structure(client_tmp):
    r = client_tmp.get("/v1/last30days", headers={"Authorization": "Bearer " + "k" * 32})
    assert r.status_code == 200
    d = r.json()["data"]
    assert "by_day" in d and isinstance(d["by_day"], list)
    assert "by_agent_top5" in d
    assert "by_kind" in d
    assert "total_events" in d


def test_costs_summary_include_raw(client_tmp):
    _clear_cost_cache()
    r0 = client_tmp.get("/v1/costs/summary?include_raw=0", headers={"Authorization": "Bearer " + "k" * 32})
    assert r0.status_code == 200
    assert "raw_tail" not in r0.json()["data"]

    _clear_cost_cache()
    r1 = client_tmp.get("/v1/costs/summary?include_raw=1", headers={"Authorization": "Bearer " + "k" * 32})
    assert r1.status_code == 200
    assert "raw_tail" in r1.json()["data"]
    assert r1.json()["data"].get("agents_normalized")


def test_state_dossier_aggregate(client_v12):
    r = client_v12.get("/v1/state/dossier/d1", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert d["dossier_id"] == "d1"
    assert len(d["tasks"]) == 2
    ids = {t["id"] for t in d["tasks"]}
    assert ids == {"td-open", "td-done"}
    assert len(d["handoffs"]) == 1
    assert d["handoffs"][0]["id"] == "ho-d1"
    assert len(d["events"]) == 2
    m = d["metrics"]
    assert m["tasks_open"] == 1
    assert m["tasks_closed"] == 1
    assert m["handoffs_pending"] == 1
    assert m["last_event_ts"]
    assert m.get("events_truncated") is False


def test_pending_approvals_filters_by_status(client_v12):
    r = client_v12.get("/v1/state/pending_approvals", headers=HDR)
    assert r.status_code == 200
    items = r.json()["data"]["items"]
    ags = {str(x.get("ag")) for x in items}
    assert "AG-12" in ags
    assert all(str(x.get("status", "")).lower() == "pending" for x in items)


def test_heartbeats_parse_openclaw(client_v12):
    r = client_v12.get("/v1/openclaw/heartbeats", headers=HDR)
    assert r.status_code == 200
    items = r.json()["data"]["items"]
    assert len(items) == 1
    jarvis = next(x for x in items if x.get("id") == "jarvis")
    assert jarvis.get("every") == "30m"
    assert jarvis.get("next_due_estimate")


def test_state_summary_counters(client_v12):
    r = client_v12.get("/v1/state/summary", headers=HDR)
    assert r.status_code == 200
    s = r.json()["data"]
    assert s["open_tasks"] == 2
    assert s["waiting_user"] == 1
    assert s["stalled_tasks"] == 1
    assert s["open_handoffs"] == 3
    assert s["pending_approvals"] == 1
    tc = s.get("tag_counts") or {}
    assert tc.get("infra") == 1 and tc.get("demo") == 1


def test_state_tag_stats_endpoint(client_v12):
    r = client_v12.get("/v1/state/tag-stats", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    tc = d["tag_counts"]
    assert tc.get("infra") == 1 and tc.get("demo") == 1
    assert d["unique_tags"] == 2


def test_state_activity_limit_50(client_v12):
    r = client_v12.get("/v1/state/activity?limit=50", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "events" in d
    assert isinstance(d["events"], list)


def test_state_activity_limit_300(client_v12):
    r = client_v12.get("/v1/state/activity?limit=300", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "events" in d
    assert isinstance(d["events"], list)


@pytest.fixture
def client_v13(tmp_path, monkeypatch, jwt_ok):
    """Repo extendido v1.3 con timestamps relativos a now y task con tags[]."""
    monkeypatch.setenv("JMC_REPO_ROOT", str(tmp_path))
    monkeypatch.setenv("JMC_OPENCLAW_JSON_PATH", str(tmp_path / "openclaw.json"))
    _clear_repo_cache()
    _seed_repo_base(tmp_path)
    (tmp_path / "openclaw.json").write_text(
        json.dumps(
            {
                "agents": {
                    "list": [
                        {"id": "jarvis", "workspace": "./agents/jarvis"},
                        {"id": "sales-hunter", "workspace": "./agents/ventas"},
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    now = datetime.now(timezone.utc)
    recent1 = (now - timedelta(hours=1)).isoformat().replace("+00:00", "Z")
    recent2 = (now - timedelta(hours=2)).isoformat().replace("+00:00", "Z")
    old = (now - timedelta(hours=30)).isoformat().replace("+00:00", "Z")
    log = (
        json.dumps({"ts": recent1, "agent": "jarvis", "type": "heartbeat", "task_id": "t1"}) + "\n"
        + json.dumps({"ts": recent2, "agent": "jarvis", "type": "start", "task_id": "t1"}) + "\n"
        + json.dumps({"ts": old, "agent": "jarvis", "type": "event"}) + "\n"
    )
    (tmp_path / "state" / "activity-log.jsonl").write_text(log, encoding="utf-8")
    (tmp_path / "state" / "tasks" / "t1.json").write_text(
        json.dumps(
            {
                "id": "t1",
                "status": "in_progress",
                "owner": "jarvis",
                "started_at": recent2,
                "tags": ["urgent", "marketing"],
                "title": "tagged task",
            }
        ),
        encoding="utf-8",
    )
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


def test_gateway_runtime_basic(client_v13):
    r = client_v13.get("/v1/openclaw/gateway?window_hours=24", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert d["window_hours"] == 24
    assert d["totals"]["events_24h"] == 2
    by_kind = {k["kind"]: k["count"] for k in d["totals"]["by_kind"]}
    assert by_kind.get("heartbeat") == 1
    assert by_kind.get("start") == 1
    by_agent = {a["id"]: a for a in d["agents"]}
    j = by_agent["jarvis"]
    assert j["events_24h"] == 2
    assert j["heartbeats_24h"] == 1
    assert j["silent"] is False
    assert j["configured"] is True
    sh = by_agent["sales-hunter"]
    assert sh["silent"] is True
    assert sh["events_24h"] == 0
    assert sh["configured"] is True


def test_gateway_window_filters_old_events(client_v13):
    r = client_v13.get("/v1/openclaw/gateway?window_hours=24", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    by_kind = {k["kind"]: k["count"] for k in d["totals"]["by_kind"]}
    assert "event" not in by_kind, "evento de hace 30h no debe entrar en ventana 24h"
    assert d["totals"]["events_24h"] == 2


def test_tasks_preserve_tags_field(client_v13):
    r = client_v13.get("/v1/state/tasks", headers=HDR)
    assert r.status_code == 200
    tasks = r.json()["data"]["tasks"]
    t1 = next(t for t in tasks if t.get("id") == "t1")
    assert t1.get("tags") == ["urgent", "marketing"]


def test_jsonl_skips_oversize_line(tmp_path):
    from app.services.jsonl_reader import iter_activity_jsonl

    p = tmp_path / "a.jsonl"
    huge = "x" * (256 * 1024 + 50)
    p.write_text(
        '{"ts":"2026-01-01T00:00:00Z","ok":1}\n'
        + huge
        + "\n"
        '{"ts":"2026-01-02T00:00:00Z","ok":2}\n',
        encoding="utf-8",
    )
    evs = list(iter_activity_jsonl(p))
    assert len(evs) == 2
    assert evs[0].get("ok") == 1 and evs[1].get("ok") == 2


def test_dossiers_skips_oversize_file(client_tmp):
    from app.config import get_repo_root

    root = get_repo_root()
    huge_path = root / "client-dossiers" / "cli-huge.json"
    huge_path.write_bytes(b'{"pad": "' + b"x" * 600_000 + b'"}')

    r = client_tmp.get("/v1/dossiers", headers=HDR)
    assert r.status_code == 200
    items = r.json()["data"]["items"]
    huge = next(x for x in items if x.get("id") == "cli-huge")
    assert huge.get("error") == "too_large"
    cli = next(x for x in items if x.get("id") == "cli-test")
    assert "data" in cli and cli["data"].get("consumerKey") == "[redacted]"


# --- JMC v1.9 (tenacitOS-inspired) ---


def test_health_includes_brand(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_BRAND_NAME", "Test MC")
    monkeypatch.setenv("JMC_BRAND_EMOJI", "🧪")
    r = client_tmp.get("/v1/health", headers=HDR)
    assert r.status_code == 200
    b = r.json()["data"].get("brand") or {}
    assert b.get("name") == "Test MC"
    assert b.get("emoji") == "🧪"


def test_auth_lockout_after_failures(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_AUTH_FAIL_MAX", "3")
    monkeypatch.setenv("JMC_AUTH_FAIL_WINDOW", "900")
    bad = {"Authorization": "Bearer " + "z" * 32}
    assert client_tmp.get("/v1/health", headers=bad).status_code == 401
    assert client_tmp.get("/v1/health", headers=bad).status_code == 401
    assert client_tmp.get("/v1/health", headers=bad).status_code == 401
    r4 = client_tmp.get("/v1/health", headers=bad)
    assert r4.status_code == 429
    assert r4.json()["detail"]["error"]["code"] == "auth_locked"


def test_system_metrics_shape(client_tmp, monkeypatch):
    import app.services.system_metrics as sm

    fake = MagicMock()
    fake.cpu_percent = lambda interval=0.1: 7.5
    fake_mem = MagicMock()
    fake_mem.used = 1000
    fake_mem.total = 8000
    fake_mem.percent = 12.5
    fake.virtual_memory = lambda: fake_mem
    fake.disk_partitions = lambda all=False: []
    fake.net_io_counters = lambda: MagicMock(bytes_sent=1, bytes_recv=2)
    fake.boot_time = lambda: 1.0
    monkeypatch.setattr(sm, "psutil", fake)
    with sm._CACHE_LOCK:
        sm._CACHE = None  # noqa: SLF001

    r = client_tmp.get("/v1/system/metrics", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert d["cpu_percent"] == 7.5
    assert d["mem"]["used"] == 1000
    assert "uptime_sec" in d


def test_runtime_services_empty_default(client_tmp, monkeypatch):
    monkeypatch.delenv("JMC_RUNTIME_SERVICES", raising=False)
    r = client_tmp.get("/v1/runtime/services", headers=HDR)
    assert r.status_code == 200
    assert r.json()["data"]["services"] == []


def test_cron_timeline_grid_shape(client_tmp):
    r = client_tmp.get("/v1/openclaw/cron-timeline?days=7", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert d["window_days"] == 7
    assert d["hours_total"] == 7 * 24
    assert isinstance(d["agents"], list)
    assert "runs_recent" in d


def test_memory_list_and_file(client_tmp):
    from app.config import get_repo_root

    root = get_repo_root()
    mem = root / "agents" / "jarvis" / "MEMORY.md"
    mem.parent.mkdir(parents=True, exist_ok=True)
    mem.write_text("# Demo\nautonomy_mode: D\n", encoding="utf-8")

    r = client_tmp.get("/v1/memory/list", headers=HDR)
    assert r.status_code == 200
    items = r.json()["data"]["items"]
    assert any(x.get("rel_path") == "agents/jarvis/MEMORY.md" for x in items)

    r2 = client_tmp.get("/v1/memory/file?path=agents/jarvis/MEMORY.md", headers=HDR)
    assert r2.status_code == 200
    assert "Demo" in (r2.json()["data"].get("content") or "")


def test_memory_file_rejects_escape(client_tmp):
    r = client_tmp.get("/v1/memory/file?path=agents/../../../etc/passwd", headers=HDR)
    assert r.status_code == 404


def test_files_tree_docs(client_tmp):
    r = client_tmp.get("/v1/files/tree?root=docs", headers=HDR)
    assert r.status_code == 200
    entries = r.json()["data"]["entries"]
    assert isinstance(entries, list)
    assert any((e.get("type") == "file" and str(e.get("path", "")).endswith(".md")) for e in entries)


def test_files_invalid_root_422(client_tmp):
    r = client_tmp.get("/v1/files/tree?root=evil", headers=HDR)
    assert r.status_code == 422


def test_search_finds_token(client_tmp):
    from app.config import get_repo_root

    marker = "jmc_search_marker_unique_abc123"
    p = get_repo_root() / "docs" / "AUTONOMIA_MODOS.md"
    txt = p.read_text(encoding="utf-8")
    if marker not in txt:
        p.write_text(txt + "\n\n" + marker + "\n", encoding="utf-8")
    r = client_tmp.get("/v1/search/?q=" + marker, headers=HDR)
    assert r.status_code == 200
    hits = r.json()["data"]["hits"]
    assert any(marker in h.get("snippet", "") for h in hits)


def test_search_short_query_empty(client_tmp):
    r = client_tmp.get("/v1/search/?q=a", headers=HDR)
    assert r.status_code == 200
    assert r.json()["data"]["hits"] == []


# --- JMC v1.10 ---


def test_health_deep_shape(client_tmp):
    r = client_tmp.get("/v1/health/deep", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "openclaw_json" in d and "activity_log" in d


def test_diagnostics_shape(client_tmp):
    r = client_tmp.get("/v1/diagnostics", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "python" in d and "repo_root" in d


def test_auth_status_open(client_tmp):
    r = client_tmp.get("/v1/auth/status")
    assert r.status_code == 200
    body = r.json()
    assert body["meta"]["version"] == "v1"
    assert "locked" in body["data"]
    assert "ip" not in body["data"]
    d = body["data"]
    assert d.get("inbound_locked") is False
    assert "inbound_fails" in d and "inbound_retry_after_sec" in d


def test_auth_status_after_lock(client_tmp, monkeypatch):
    # get_auth_fail_max() fuerza mínimo 3 → hacen falta 3×401 y luego 429.
    monkeypatch.setenv("JMC_AUTH_FAIL_MAX", "2")
    monkeypatch.setenv("JMC_AUTH_FAIL_WINDOW", "900")
    bad = {"Authorization": "Bearer " + "z" * 32}
    assert client_tmp.get("/v1/health", headers=bad).status_code == 401
    assert client_tmp.get("/v1/health", headers=bad).status_code == 401
    assert client_tmp.get("/v1/health", headers=bad).status_code == 401
    assert client_tmp.get("/v1/health", headers=bad).status_code == 429
    s = client_tmp.get("/v1/auth/status")
    assert s.status_code == 200
    assert s.json()["data"].get("locked") is True


def test_files_get_docs_ok(client_tmp):
    r = client_tmp.get("/v1/files/get", headers=HDR, params={"root": "docs", "path": "APPROVAL_GATES.md"})
    assert r.status_code == 200
    assert "AG-01" in r.json()["data"]["content"]


def test_files_get_invalid_root_422(client_tmp):
    r = client_tmp.get("/v1/files/get", headers=HDR, params={"root": "state", "path": "x"})
    assert r.status_code == 422


def test_webhooks_notify_not_configured(client_tmp):
    r = client_tmp.post("/v1/webhooks/notify", headers=HDR, json={"hello": 1})
    assert r.status_code == 200
    d = r.json()["data"]
    assert d.get("sent") is False


def test_webhooks_notify_sent_mock(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_WEBHOOK_URL", "https://example.com/webhook")

    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def getcode(self):
            return 204

    def fake_urlopen(req, timeout=5.0):
        return _Resp()

    monkeypatch.setattr("app.services.webhook_send.urllib.request.urlopen", fake_urlopen)
    r = client_tmp.post("/v1/webhooks/notify", headers=HDR, json={"x": 1})
    assert r.status_code == 200
    assert r.json()["data"].get("sent") is True


def test_webhooks_url_rejects_non_http(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_WEBHOOK_URL", "file:///etc/passwd")
    r = client_tmp.post("/v1/webhooks/notify", headers=HDR, json={})
    assert r.status_code == 200
    assert r.json()["data"].get("sent") is False


def test_webhooks_status_ok(client_tmp):
    r = client_tmp.get("/v1/webhooks/status", headers=HDR)
    assert r.status_code == 200
    body = r.json()
    assert body["meta"]["version"] == "v1"
    assert "configured" in body["data"]
    assert isinstance(body["data"]["configured"], bool)


def test_webhooks_notify_blocks_private_ip(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_WEBHOOK_URL", "http://192.168.0.1/webhook")
    r = client_tmp.post("/v1/webhooks/notify", headers=HDR, json={"x": 1})
    assert r.status_code == 200
    d = r.json()["data"]
    assert d.get("sent") is False
    assert d.get("error") == "webhook_host_not_allowed"


def test_costs_by_agent_smoke(client_tmp):
    _clear_cost_cache()
    r = client_tmp.get("/v1/costs/by-agent", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "agents" in d
    assert any(a.get("agent") == "jarvis" for a in d["agents"])


def test_csp_report_caps(client_tmp):
    from app.services import csp_report_store as csp

    csp.reset_csp_reports_for_tests()
    for _ in range(520):
        assert client_tmp.post("/v1/csp-report", json={"x": 1}).status_code == 200
    assert len(csp._reports) <= 500  # noqa: SLF001


def test_agents_stats_top_n(client_v12):
    r = client_v12.get("/v1/state/agents-stats", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "top_agents_24h" in d and "top_errors_24h" in d


def test_state_zombies_threshold(client_v12):
    r = client_v12.get("/v1/state/zombies?hours=1", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert d.get("threshold_hours") == 1.0
    assert "items" in d


def test_state_latency_basic(client_v12):
    r = client_v12.get("/v1/state/latency", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "by_agent" in d and "by_dossier" in d


def test_skills_coverage_basic(client_tmp):
    r = client_tmp.get("/v1/skills/coverage", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    rows = d["agents"]
    assert any(r.get("agent_id") == "jarvis" for r in rows)
    assert "by_workspace" in d
    bw = d.get("by_workspace") or []
    assert any((x.get("workspace") or "").endswith("agents/jarvis") for x in bw)


def test_skills_coverage_absolute_workspace(tmp_path, monkeypatch, jwt_ok):
    """Workspace absoluto bajo el mismo repo (como ~/.openclaw con paths home) debe resolverse vía sufijo agents/."""
    monkeypatch.setenv("JMC_REPO_ROOT", str(tmp_path))
    oc = tmp_path / "openclaw.json"
    jar = tmp_path / "agents" / "jarvis" / "skills" / "abs-skill"
    jar.mkdir(parents=True)
    (jar / "SKILL.md").write_text("---\nname: abs\n---\n", encoding="utf-8")
    fake_home = str(tmp_path / "fake-home" / "jarvis-ecosystem" / "agents" / "jarvis")
    oc.write_text(
        json.dumps({"agents": {"list": [{"id": "jarvis", "workspace": fake_home}]}}),
        encoding="utf-8",
    )
    monkeypatch.setenv("JMC_OPENCLAW_JSON_PATH", str(oc))
    _clear_repo_cache()
    from fastapi.testclient import TestClient

    from app.main import app

    c = TestClient(app)
    r = c.get("/v1/skills/coverage", headers=HDR)
    assert r.status_code == 200
    row = next(x for x in r.json()["data"]["agents"] if x.get("agent_id") == "jarvis")
    assert row.get("skill_md_count") == 1
    assert row.get("resolved_workspace") == "agents/jarvis"


def test_inbound_telegram_503_without_secret(client_tmp, monkeypatch):
    monkeypatch.delenv("JMC_INBOUND_TELEGRAM_SECRET", raising=False)
    monkeypatch.delenv("JMC_INBOUND_CHANNEL_SECRET", raising=False)
    r = client_tmp.post(
        "/v1/webhooks/inbound/telegram",
        json={"text": "hola"},
        headers={"X-JMC-Inbound-Secret": "x" * 20},
    )
    assert r.status_code == 503


def test_inbound_telegram_401_bad_secret(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_INBOUND_TELEGRAM_SECRET", "a" * 20)
    r = client_tmp.post(
        "/v1/webhooks/inbound/telegram",
        json={"text": "hola"},
        headers={"X-JMC-Inbound-Secret": "b" * 20},
    )
    assert r.status_code == 401


def test_inbound_telegram_ok_monkeypatch(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_INBOUND_TELEGRAM_SECRET", "s" * 20)
    calls: list = []

    def fake_append(**kw):
        calls.append(kw)
        return {"ok": True, "agent": kw.get("agent")}

    monkeypatch.setattr("app.routers.inbound.append_messaging_channel_event", fake_append)
    r = client_tmp.post(
        "/v1/webhooks/inbound/telegram",
        json={"text": "ping", "direction": "in", "agent": "jarvis"},
        headers={"X-JMC-Inbound-Secret": "s" * 20},
    )
    assert r.status_code == 200
    assert calls and calls[0]["agent"] == "jarvis"
    assert calls[0].get("channel") == "telegram"


def test_inbound_whatsapp_ok_monkeypatch(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_INBOUND_TELEGRAM_SECRET", "s" * 20)
    calls: list = []

    def fake_append(**kw):
        calls.append(kw)
        return {"ok": True, "agent": kw.get("agent")}

    monkeypatch.setattr("app.routers.inbound.append_messaging_channel_event", fake_append)
    r = client_tmp.post(
        "/v1/webhooks/inbound/whatsapp",
        json={"text": "hola", "direction": "in", "agent": "jarvis"},
        headers={"X-JMC-Inbound-Secret": "s" * 20},
    )
    assert r.status_code == 200
    assert calls[0].get("channel") == "whatsapp"


def test_inbound_discord_ok_monkeypatch(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_INBOUND_TELEGRAM_SECRET", "s" * 20)
    calls: list = []

    def fake_append(**kw):
        calls.append(kw)
        return {"ok": True, "agent": kw.get("agent")}

    monkeypatch.setattr("app.routers.inbound.append_messaging_channel_event", fake_append)
    r = client_tmp.post(
        "/v1/webhooks/inbound/discord",
        json={"text": "hola discord", "direction": "in", "agent": "jarvis"},
        headers={"X-JMC-Inbound-Secret": "s" * 20},
    )
    assert r.status_code == 200
    assert calls[0].get("channel") == "discord"


def test_inbound_lockout_after_bad_secrets(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_INBOUND_TELEGRAM_SECRET", "goodsecretgoodsecret12")
    monkeypatch.setenv("JMC_AUTH_FAIL_MAX", "3")
    monkeypatch.setenv("JMC_AUTH_FAIL_WINDOW", "900")
    hdr_bad = {"X-JMC-Inbound-Secret": "wrongwrongwrongwrong1"}
    for _ in range(3):
        assert client_tmp.post("/v1/webhooks/inbound/telegram", json={"text": "x"}, headers=hdr_bad).status_code == 401
    r4 = client_tmp.post("/v1/webhooks/inbound/telegram", json={"text": "x"}, headers=hdr_bad)
    assert r4.status_code == 429


def test_inbound_bad_secret_wrong_length_still_401(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_INBOUND_TELEGRAM_SECRET", "s" * 24)
    r = client_tmp.post(
        "/v1/webhooks/inbound/telegram",
        json={"text": "x"},
        headers={"X-JMC-Inbound-Secret": "s" * 10},
    )
    assert r.status_code == 401


def test_inbound_invalid_channel_422(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_INBOUND_TELEGRAM_SECRET", "s" * 20)
    r = client_tmp.post(
        "/v1/webhooks/inbound/slack",
        json={"text": "x"},
        headers={"X-JMC-Inbound-Secret": "s" * 20},
    )
    assert r.status_code == 422


def test_heartbeats_coverage_missing(client_tmp):
    r = client_tmp.get("/v1/heartbeats/coverage", headers=HDR)
    assert r.status_code == 200
    miss = r.json()["data"].get("missing_heartbeat") or []
    assert "jarvis" in miss


def test_docs_lints_consistency(client_tmp):
    r = client_tmp.get("/v1/docs/lints", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "ok" in d and "in_gates_not_matrix" in d


def test_system_cpu_detail_mock(client_tmp, monkeypatch):
    import app.services.system_metrics_extra as smx

    monkeypatch.setattr(smx.psutil, "cpu_percent", lambda interval=0, percpu=True: [1.0, 2.0])
    r = client_tmp.get("/v1/system/cpu-detail", headers=HDR)
    assert r.status_code == 200
    assert r.json()["data"]["count"] == 2


def test_system_proc_summary_mock(client_tmp, monkeypatch):
    import app.services.system_metrics_extra as smx

    class P:
        def __init__(self):
            self.info = {"memory_info": MagicMock(rss=4096)}

        def __iter__(self):
            return iter([P(), P()])

    monkeypatch.setattr(smx.psutil, "process_iter", lambda attrs=None: iter([P(), P()]))
    r = client_tmp.get("/v1/system/proc-summary", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert d.get("processes_scanned") == 2


def test_system_fs_latency(client_tmp):
    r = client_tmp.get("/v1/system/fs-latency", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert d.get("stat_ms") is not None or d.get("error")


def test_external_healthchecks_invalid_scheme(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_EXT_HEALTHCHECKS", "x|ftp://bad.example")
    r = client_tmp.get("/v1/external/healthchecks", headers=HDR)
    assert r.status_code == 200
    items = r.json()["data"]["items"]
    assert items and items[0].get("error") == "invalid_scheme"


def test_external_healthchecks_block_private(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_EXT_HEALTHCHECKS", "p|http://192.168.0.1/")
    r = client_tmp.get("/v1/external/healthchecks", headers=HDR)
    assert r.status_code == 200
    assert r.json()["data"]["items"][0].get("error") == "host_not_allowed"


def test_runtime_services_logs_opt_in(client_tmp, monkeypatch):
    from app.services import runtime_services as rs

    monkeypatch.setenv("JMC_RUNTIME_SERVICES", "foo.service")
    monkeypatch.setenv("JMC_RUNTIME_LOGS", "1")
    monkeypatch.setattr(rs, "journal_tail", lambda unit, lines: {"unit": unit, "lines": lines, "text": "ok"})
    r = client_tmp.get("/v1/runtime/services?journal_lines=5", headers=HDR)
    assert r.status_code == 200
    svcs = r.json()["data"]["services"]
    assert svcs and "journal" in svcs[0]


def test_webhook_disabled_when_unset(client_tmp):
    r = client_tmp.post("/v1/webhooks/test", headers=HDR)
    assert r.status_code == 200
    assert r.json()["data"].get("sent") is False


def test_brand_extra_fields(client_tmp, monkeypatch):
    monkeypatch.setenv("JMC_BRAND_DESCRIPTION", "Desc test")
    monkeypatch.setenv("JMC_BRAND_LOCATION", "Madrid")
    monkeypatch.setenv("JMC_BRAND_BIRTH_DATE", "2020-01-01")
    monkeypatch.setenv("JMC_BRAND_TWITTER", "@x")
    r = client_tmp.get("/v1/health", headers=HDR)
    b = r.json()["data"]["brand"]
    assert b.get("description") == "Desc test"
    assert b.get("location") == "Madrid"
    assert b.get("birth_date") == "2020-01-01"
    assert b.get("social") == "@x"


def test_memory_list_stale_field(client_tmp):
    r = client_tmp.get("/v1/memory/list", headers=HDR)
    assert r.status_code == 200
    for it in r.json()["data"]["items"]:
        assert "stale" in it
        assert "stale_after_days" in it
