"""Buzón JMC Chat bajo `state/jmc-inbox/` (o `JMC_CHAT_INBOX_DIR`)."""

from __future__ import annotations

import asyncio
import json
import os
import re
import secrets
import shutil
import tempfile
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.security import allowed_path
from app.services import chat_attachments
from app.services.paths import chat_inbox_dir
from app.services.read_capped import read_capped_text
from app.services.telegram_inbound import append_activity_log_event

_CONV_ID = re.compile(r"^conv-\d{4}-\d{2}-\d{2}-[a-f0-9]{6}$")
_MSG_STEM = re.compile(r"^msg-\d{4}-\d{2}-\d{2}-\d{6}-[a-f0-9]{6}$")

_conv_post_locks: dict[str, asyncio.Lock] = {}
_locks_guard = asyncio.Lock()


def mirror_result_for_persist(mr: dict[str, Any] | None) -> dict[str, Any] | None:
    """Omite salida de proceso y detalles internos antes de persistir o loguear."""
    if mr is None:
        return None
    drop = frozenset({"stderr", "stdout", "detail", "path"})
    return {k: v for k, v in mr.items() if k not in drop}


@asynccontextmanager
async def conv_post_guard(conv_id: str):
    """Serializa POST de mensaje + adjuntos por conversación."""
    assert_conv_id(conv_id)
    async with _locks_guard:
        if conv_id not in _conv_post_locks:
            _conv_post_locks[conv_id] = asyncio.Lock()
        lock = _conv_post_locks[conv_id]
    async with lock:
        yield


def inbox_root() -> Path:
    p = chat_inbox_dir()
    p.mkdir(parents=True, exist_ok=True)
    (p / "_archived").mkdir(exist_ok=True)
    return p


def _roots() -> tuple[Path, ...]:
    return (inbox_root().resolve(),)


def assert_conv_id(conv_id: str) -> None:
    if not _CONV_ID.fullmatch(conv_id or ""):
        raise ValueError("invalid_conv_id")


def assert_msg_id(msg_id: str) -> None:
    if not _MSG_STEM.fullmatch(msg_id or ""):
        raise ValueError("invalid_msg_id")


def conv_dir(conv_id: str) -> Path:
    assert_conv_id(conv_id)
    d = (inbox_root() / conv_id).resolve()
    try:
        d.relative_to(inbox_root().resolve())
    except ValueError as e:
        raise ValueError("invalid_path") from e
    if not allowed_path(d, _roots()):
        raise ValueError("invalid_path")
    return d


def new_conv_id() -> str:
    d = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for _ in range(32):
        cid = f"conv-{d}-{secrets.token_hex(3)}"
        if _CONV_ID.fullmatch(cid):
            return cid
    raise RuntimeError("conv_id_generation_failed")


def new_msg_id() -> str:
    d = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    t = datetime.now(timezone.utc).strftime("%H%M%S")
    return f"msg-{d}-{t}-{secrets.token_hex(3)}"


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    """Escribe JSON de forma atómica (temp + os.replace) para evitar meta/mensajes a medias."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    fd, tmp_name = tempfile.mkstemp(prefix=".jmc-inbox-", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as wf:
            wf.write(text)
        os.replace(str(tmp_path), str(path))
    except Exception:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def attachment_dir_for_message(conv_id: str, msg_id: str) -> Path:
    assert_conv_id(conv_id)
    assert_msg_id(msg_id)
    return conv_dir(conv_id) / f"{msg_id}.attachments"


def create_conversation(*, title: str | None = None) -> dict[str, Any]:
    for _ in range(32):
        cid = new_conv_id()
        d = inbox_root() / cid
        if d.exists():
            continue
        d.mkdir(parents=True, exist_ok=False)
        meta = {
            "conv_id": cid,
            "title": (title or "Chat").strip()[:200] or "Chat",
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "archived": False,
        }
        _atomic_write_json(d / "meta.json", meta)
        return meta
    raise RuntimeError("create_conversation_failed")


def list_conversations() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    root = inbox_root()
    roots = _roots()
    for p in sorted(root.iterdir()):
        if p.name.startswith("_") or not p.is_dir():
            continue
        if not _CONV_ID.fullmatch(p.name):
            continue
        if not allowed_path(p, roots):
            continue
        meta_path = p / "meta.json"
        if meta_path.is_file():
            txt = read_capped_text(meta_path, max_bytes=256_000)
            if txt:
                try:
                    meta = json.loads(txt)
                    if isinstance(meta, dict):
                        items.append(meta)
                        continue
                except json.JSONDecodeError:
                    pass
        items.append({"conv_id": p.name, "title": p.name, "created_at": None, "archived": False})
    items.sort(key=lambda x: str(x.get("created_at") or x.get("conv_id") or ""), reverse=True)
    return items


def _is_msg_json_filename(name: str) -> bool:
    if not name.endswith(".json") or name.endswith(".reply.json"):
        return False
    return bool(_MSG_STEM.fullmatch(name[:-5]))


def read_conversation(conv_id: str) -> dict[str, Any]:
    d = conv_dir(conv_id)
    if not d.is_dir():
        raise FileNotFoundError(conv_id)
    meta: dict[str, Any] = {}
    mp = d / "meta.json"
    if mp.is_file():
        txt = read_capped_text(mp, max_bytes=256_000)
        if txt:
            try:
                loaded = json.loads(txt)
                if isinstance(loaded, dict):
                    meta = loaded
            except json.JSONDecodeError:
                meta = {}
    messages: list[dict[str, Any]] = []
    roots = _roots()
    for f in sorted(d.glob("msg-*.json")):
        if f.name.endswith(".reply.json"):
            continue
        if not _is_msg_json_filename(f.name):
            continue
        if not allowed_path(f, roots):
            continue
        txt = read_capped_text(f, max_bytes=2 * 1024 * 1024)
        if not txt:
            continue
        try:
            msg = json.loads(txt)
        except json.JSONDecodeError:
            continue
        if not isinstance(msg, dict):
            continue
        stem = f.stem
        reply_path = d / f"{stem}.reply.json"
        reply: dict[str, Any] | None = None
        if reply_path.is_file() and allowed_path(reply_path, roots):
            rt = read_capped_text(reply_path, max_bytes=2 * 1024 * 1024)
            if rt:
                try:
                    loaded = json.loads(rt)
                    reply = loaded if isinstance(loaded, dict) else None
                except json.JSONDecodeError:
                    reply = None
        messages.append({"message": msg, "reply": reply})
    return {"conv_id": conv_id, "meta": meta, "messages": messages}


def archive_conversation(conv_id: str) -> dict[str, Any]:
    d = conv_dir(conv_id)
    if not d.is_dir():
        raise FileNotFoundError(conv_id)
    arch = inbox_root() / "_archived" / conv_id
    arch.parent.mkdir(parents=True, exist_ok=True)
    if arch.exists():
        shutil.rmtree(arch, ignore_errors=True)
    shutil.move(str(d), str(arch))
    return {"conv_id": conv_id, "archived_to": str(arch)}


def write_message_record(
    conv_id: str,
    msg_id: str,
    *,
    text: str,
    attachments_meta: list[dict[str, Any]],
    mirror_channel: str | None,
    mirror_result: dict[str, Any] | None,
) -> dict[str, Any]:
    assert_conv_id(conv_id)
    assert_msg_id(msg_id)
    d = conv_dir(conv_id)
    if not d.is_dir():
        raise FileNotFoundError(conv_id)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    body: dict[str, Any] = {
        "id": msg_id,
        "role": "ceo",
        "text": (text or "")[:100_000],
        "ts": now,
        "attachments": attachments_meta,
    }
    if mirror_channel:
        body["mirror_channel"] = mirror_channel.strip().lower()[:32]
    if mirror_result is not None:
        body["mirror_result"] = mirror_result_for_persist(mirror_result)
    msg_path = d / f"{msg_id}.json"
    _atomic_write_json(msg_path, body)
    note = f"{msg_id}: {(text or '')[:300]}"
    payload: dict[str, Any] = {
        "conv_id": conv_id,
        "msg_id": msg_id,
        "attachment_count": len(attachments_meta),
    }
    if mirror_result is not None:
        payload["mirror"] = mirror_result_for_persist(mirror_result)
    log_r = append_activity_log_event(
        agent="ceo",
        task=f"jmc-chat-{conv_id}",
        kind="jmc_inbox",
        note=note,
        payload=payload,
    )
    return {"message": body, "activity_log": log_r}


def resolve_attachment_path(conv_id: str, msg_id: str, filename: str) -> Path:
    assert_conv_id(conv_id)
    assert_msg_id(msg_id)
    safe = chat_attachments.sanitize_basename(filename)
    att = conv_dir(conv_id) / f"{msg_id}.attachments" / safe
    roots = (inbox_root().resolve(),)
    if not allowed_path(att, roots):
        raise ValueError("path_not_allowed")
    return att
