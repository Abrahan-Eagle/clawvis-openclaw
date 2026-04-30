"""Tests del buzón JMC Chat (`/v1/chat/*`)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

import test_endpoints as te

HDR = {"Authorization": "Bearer " + "k" * 32}


@pytest.fixture
def client_chat(tmp_path, monkeypatch):
    monkeypatch.setenv("JMC_BEARER_TOKEN", "k" * 32)
    monkeypatch.setenv("JMC_REPO_ROOT", str(tmp_path))
    monkeypatch.setenv("JMC_OPENCLAW_JSON_PATH", str(tmp_path / "openclaw.json"))
    te._clear_repo_cache()
    te._seed_repo_base(tmp_path)
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


@pytest.fixture
def log_calls(monkeypatch):
    calls: list[dict] = []

    def _fake(**kw):
        calls.append(kw)
        return {"ok": True, "mocked": True}

    monkeypatch.setattr("app.services.chat_inbox.append_activity_log_event", _fake)
    return calls


def _create_conv(client) -> str:
    r = client.post("/v1/chat/conversations", json={"title": "t1"}, headers=HDR)
    assert r.status_code == 200
    return r.json()["data"]["conv_id"]


def test_post_message_no_attachments_200_and_activity(client_chat, log_calls):
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "hola jarvis"},
        headers=HDR,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["data"]["message"]["text"] == "hola jarvis"
    assert body["data"]["message"]["role"] == "ceo"
    msg_id = body["data"]["msg_id"]
    assert msg_id.startswith("msg-")
    from app.config import get_repo_root

    conv_dir = get_repo_root() / "state" / "jmc-inbox" / cid
    mp = conv_dir / f"{msg_id}.json"
    assert mp.is_file()
    assert len(log_calls) == 1
    assert log_calls[0]["kind"] == "jmc_inbox"
    assert log_calls[0]["task"] == f"jmc-chat-{cid}"
    assert log_calls[0]["payload"]["conv_id"] == cid


def test_post_message_with_one_attachment(client_chat, log_calls):
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "con doc"},
        files=[("files", ("note.txt", b"hello", "text/plain"))],
        headers=HDR,
    )
    assert r.status_code == 200
    msg_id = r.json()["data"]["msg_id"]
    from app.config import get_repo_root

    att_dir = get_repo_root() / "state" / "jmc-inbox" / cid / f"{msg_id}.attachments"
    assert att_dir.is_dir()
    txts = list(att_dir.glob("*.txt"))
    assert len(txts) == 1
    assert txts[0].read_bytes() == b"hello"


def test_post_file_too_large_413(client_chat, monkeypatch, log_calls):
    # Mínimo efectivo del servicio: 1024 bytes (ver chat_attachments.max_file_bytes)
    monkeypatch.setenv("JMC_CHAT_MAX_FILE_BYTES", "2000")
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "x"},
        files=[("files", ("big.txt", b"x" * 5000, "text/plain"))],
        headers=HDR,
    )
    assert r.status_code == 413


def test_post_blocked_extension_422(client_chat, log_calls):
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "x"},
        files=[("files", ("evil.sh", b"#!/bin/bash\n", "text/plain"))],
        headers=HDR,
    )
    assert r.status_code == 422


def test_post_too_many_files_422(client_chat, log_calls):
    cid = _create_conv(client_chat)
    files = [("files", (f"f{i}.txt", b"x", "text/plain")) for i in range(6)]
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "many"},
        files=files,
        headers=HDR,
    )
    assert r.status_code == 422


def test_get_conversation_404(client_chat):
    r = client_chat.get("/v1/chat/conversations/conv-2099-01-01-abcdef", headers=HDR)
    assert r.status_code == 404


def test_download_attachment_path_traversal_400(client_chat):
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "a"},
        files=[("files", ("ok.txt", b"1", "text/plain"))],
        headers=HDR,
    )
    msg_id = r.json()["data"]["msg_id"]
    # El router rechaza ".." y "/" en el nombre (defensa antes de sanitize basename).
    bad = client_chat.get(
        f"/v1/chat/conversations/{cid}/messages/{msg_id}/attachments/not..allowed.txt",
        headers=HDR,
    )
    assert bad.status_code == 400


def test_download_attachment_ok_200(client_chat):
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "con doc"},
        files=[("files", ("doc.txt", b"hello-bytes", "text/plain"))],
        headers=HDR,
    )
    assert r.status_code == 200
    msg_id = r.json()["data"]["msg_id"]
    dl = client_chat.get(
        f"/v1/chat/conversations/{cid}/messages/{msg_id}/attachments/doc.txt",
        headers=HDR,
    )
    assert dl.status_code == 200
    assert dl.content == b"hello-bytes"


def test_mirror_openclaw_bin_missing_warning(client_chat, monkeypatch, log_calls):
    monkeypatch.setenv("JMC_CHAT_MIRROR_ENABLED", "1")
    monkeypatch.setenv("JMC_OPENCLAW_BIN", "/nonexistent/openclaw_bin_xyz")
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "mirror me", "mirror_channel": "telegram"},
        headers=HDR,
    )
    assert r.status_code == 200
    meta = r.json()["meta"]
    assert "openclaw_bin_missing" in meta["warnings"]
    body = r.json()["data"]
    assert body["message"]["mirror_result"]["warning"] == "openclaw_bin_missing"
    assert "path" not in (body["message"].get("mirror_result") or {})
    msg_id = body["msg_id"]
    from app.config import get_repo_root

    raw = (get_repo_root() / "state" / "jmc-inbox" / cid / f"{msg_id}.json").read_text(encoding="utf-8")
    assert '"path"' not in raw


def test_post_message_activity_log_failure_redacts_stderr(client_chat, monkeypatch):
    from app.config import get_repo_root

    root = get_repo_root()
    script = root / "skills" / "global" / "activity-log" / "bin" / "activity-log"
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_text("#!/bin/bash\nexit 1\n", encoding="utf-8")
    script.chmod(0o755)

    def fake_run(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 1
        m.stderr = "SECRET_ACTIVITY_STDERR_ZZ"
        m.stdout = ""
        return m

    monkeypatch.setattr("app.services.telegram_inbound.subprocess.run", fake_run)
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "hello"},
        headers=HDR,
    )
    assert r.status_code == 200
    al = r.json()["data"].get("activity_log") or {}
    assert al.get("ok") is False
    assert "stderr" not in al
    assert "SECRET_ACTIVITY_STDERR_ZZ" not in json.dumps(r.json())


def test_chat_options_200(client_chat):
    r = client_chat.get("/v1/chat/options", headers=HDR)
    assert r.status_code == 200
    d = r.json()["data"]
    assert "mirror_enabled" in d and "max_file_bytes" in d


def test_chat_conversations_list_empty_then_one(client_chat):
    r0 = client_chat.get("/v1/chat/conversations", headers=HDR)
    assert r0.status_code == 200
    assert r0.json()["data"]["items"] == []
    cid = _create_conv(client_chat)
    r1 = client_chat.get("/v1/chat/conversations", headers=HDR)
    assert r1.status_code == 200
    ids = [x["conv_id"] for x in r1.json()["data"]["items"]]
    assert cid in ids


def test_chat_get_conversation_200_with_meta(client_chat):
    cid = _create_conv(client_chat)
    client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "uno"},
        headers=HDR,
    )
    r = client_chat.get(f"/v1/chat/conversations/{cid}", headers=HDR)
    assert r.status_code == 200
    body = r.json()["data"]
    assert body["conv_id"] == cid
    assert "meta" in body
    assert len(body["messages"]) >= 1
    assert body["messages"][-1]["message"]["text"] == "uno"


def test_chat_archive_moves_to_archived(client_chat):
    cid = _create_conv(client_chat)
    r = client_chat.post(f"/v1/chat/conversations/{cid}/archive", headers=HDR)
    assert r.status_code == 200
    from app.config import get_repo_root

    arch = get_repo_root() / "state" / "jmc-inbox" / "_archived" / cid
    assert arch.is_dir()


def test_mirror_stderr_not_persisted_on_disk(client_chat, tmp_path, monkeypatch, log_calls):
    monkeypatch.setenv("JMC_CHAT_MIRROR_ENABLED", "1")
    fake_bin = tmp_path / "openclaw_fake"
    fake_bin.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    fake_bin.chmod(0o755)
    monkeypatch.setenv("JMC_OPENCLAW_BIN", str(fake_bin))

    def fake_run(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 1
        m.stderr = "SECRET_MIRROR_STDERR_XYZ"
        m.stdout = ""
        return m

    monkeypatch.setattr("app.services.chat_mirror.subprocess.run", fake_run)
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "fail mirror", "mirror_channel": "telegram"},
        headers=HDR,
    )
    assert r.status_code == 200
    msg_id = r.json()["data"]["msg_id"]
    from app.config import get_repo_root

    mp = get_repo_root() / "state" / "jmc-inbox" / cid / f"{msg_id}.json"
    raw = mp.read_text(encoding="utf-8")
    assert "SECRET_MIRROR_STDERR_XYZ" not in raw
    assert '"stderr"' not in raw
    mr = r.json()["data"]["message"].get("mirror_result") or {}
    assert "stderr" not in mr


def test_mirror_subprocess_ok(client_chat, tmp_path, monkeypatch, log_calls):
    monkeypatch.setenv("JMC_CHAT_MIRROR_ENABLED", "1")
    fake_bin = tmp_path / "openclaw_fake"
    fake_bin.write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
    fake_bin.chmod(0o755)
    monkeypatch.setenv("JMC_OPENCLAW_BIN", str(fake_bin))

    def fake_run(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stderr = ""
        m.stdout = "sent"
        return m

    monkeypatch.setattr("app.services.chat_mirror.subprocess.run", fake_run)
    cid = _create_conv(client_chat)
    r = client_chat.post(
        f"/v1/chat/conversations/{cid}/messages",
        data={"text": "to channel", "mirror_channel": "discord"},
        headers=HDR,
    )
    assert r.status_code == 200
    assert r.json()["data"]["message"]["mirror_result"]["ok"] is True
