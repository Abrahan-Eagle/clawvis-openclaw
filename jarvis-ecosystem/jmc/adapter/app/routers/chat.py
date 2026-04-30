"""Chat JMC: buzón `state/jmc-inbox/` + adjuntos + espejo opcional OpenClaw."""

from __future__ import annotations

import logging
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.security import require_token
from app.services import chat_attachments, chat_inbox, chat_mirror
from app.util_response import envelope

router = APIRouter(prefix="/chat", dependencies=[Depends(require_token)])
_log = logging.getLogger(__name__)


@router.get("/options")
def chat_options():
    """Flags de UI (espejo OpenClaw, límites de adjuntos)."""
    return envelope(
        {
            "mirror_enabled": chat_mirror.mirror_enabled(),
            "mirror_channels": chat_mirror.mirror_channels_allowed(),
            "max_file_bytes": chat_attachments.max_file_bytes(),
            "max_files_per_message": chat_attachments.max_files_per_message(),
        }
    )


def _http_error(status: int, code: str, message: str) -> None:
    raise HTTPException(status_code=status, detail={"error": {"code": code, "message": message}})


@router.get("/conversations")
def list_conversations():
    try:
        items = chat_inbox.list_conversations()
    except OSError as e:
        _log.exception("list_conversations: %s", e)
        _http_error(500, "inbox_list_failed", "No se pudo leer el buzón de chat.")
    return envelope({"items": items})


@router.post("/conversations")
def create_conversation(body: dict = Body(default_factory=dict)):
    title = body.get("title") if isinstance(body, dict) else None
    try:
        meta = chat_inbox.create_conversation(title=str(title) if title is not None else None)
    except RuntimeError as e:
        _log.exception("create_conversation: %s", e)
        _http_error(500, "create_failed", "No se pudo crear la conversación.")
    except OSError as e:
        _log.exception("create_conversation: %s", e)
        _http_error(500, "create_failed", "No se pudo crear la conversación.")
    return envelope(meta)


@router.get("/conversations/{conv_id}")
def get_conversation(conv_id: str):
    try:
        data = chat_inbox.read_conversation(conv_id)
    except ValueError:
        _http_error(400, "invalid_conv_id", "ID de conversación no válido")
        raise
    except FileNotFoundError:
        _http_error(404, "not_found", "Conversación no encontrada")
        raise
    return envelope(data)


@router.post("/conversations/{conv_id}/archive")
def archive_conversation(conv_id: str):
    try:
        out = chat_inbox.archive_conversation(conv_id)
    except ValueError:
        _http_error(400, "invalid_conv_id", "ID de conversación no válido")
        raise
    except FileNotFoundError:
        _http_error(404, "not_found", "Conversación no encontrada")
        raise
    return envelope(out)


@router.post("/conversations/{conv_id}/messages")
async def post_message(
    conv_id: str,
    text: Annotated[str, Form()] = "",
    mirror_channel: Annotated[str | None, Form()] = None,
    files: Annotated[list[UploadFile] | None, File()] = None,
):
    warnings: list[str] = []
    upload_list = files or []
    try:
        d = chat_inbox.conv_dir(conv_id)
    except ValueError:
        _http_error(400, "invalid_conv_id", "ID de conversación no válido")
        raise
    if not d.is_dir():
        _http_error(404, "not_found", "Conversación no encontrada")
        raise

    max_n = chat_attachments.max_files_per_message()
    if len(upload_list) > max_n:
        _http_error(422, "too_many_files", f"Máximo {max_n} archivos por mensaje")
        raise

    async with chat_inbox.conv_post_guard(conv_id):
        msg_id = chat_inbox.new_msg_id()
        att_dir = chat_inbox.attachment_dir_for_message(conv_id, msg_id)
        attachments_meta: list[dict[str, Any]] = []
        max_b = chat_attachments.max_file_bytes()

        for up in upload_list:
            if not up.filename:
                continue
            try:
                safe = chat_attachments.sanitize_basename(up.filename)
            except ValueError as e:
                code = str(e)
                if code == "blocked_extension":
                    _http_error(422, "blocked_extension", "Extensión no permitida")
                if code == "extension_required":
                    _http_error(422, "extension_required", "Cada archivo debe tener extensión")
                _http_error(422, "invalid_filename", "Nombre de archivo no válido")
                raise
            dest = att_dir / safe
            try:
                att_dir.mkdir(parents=True, exist_ok=True)
                chat_attachments.save_stream_capped(up.file, dest, max_bytes=max_b)
            except ValueError as e:
                if str(e) == "file_too_large":
                    if dest.is_file():
                        try:
                            dest.unlink()
                        except OSError:
                            pass
                    _http_error(413, "file_too_large", f"Archivo supera {max_b} bytes")
                raise
            sz = dest.stat().st_size if dest.is_file() else 0
            attachments_meta.append(
                {
                    "stored_name": safe,
                    "original_name": up.filename[:500],
                    "size_bytes": sz,
                    "content_type": (up.content_type or "")[:200],
                }
            )

        mirror_result: dict[str, Any] | None = None
        ch = (mirror_channel or "").strip().lower() or None
        if ch:
            if not chat_mirror.mirror_enabled():
                warnings.append("mirror_ignored_config_disabled")
                ch = None
            elif ch not in chat_mirror.mirror_channels_allowed():
                _http_error(422, "invalid_mirror_channel", "Canal de espejo no permitido")
                raise
            else:
                mirror_lines = (text or "").strip()[:4000]
                if attachments_meta:
                    names = ", ".join(a["stored_name"] for a in attachments_meta)
                    mirror_lines = f"{mirror_lines}\n\n[Adjuntos JMC: {names}]"[:8000]
                mirror_result = chat_mirror.mirror_to_channel(channel=ch, text=mirror_lines or "(sin texto)")
                if not mirror_result.get("ok") and mirror_result.get("warning") == "openclaw_bin_missing":
                    warnings.append("openclaw_bin_missing")

        try:
            out = chat_inbox.write_message_record(
                conv_id,
                msg_id,
                text=text or "",
                attachments_meta=attachments_meta,
                mirror_channel=ch,
                mirror_result=mirror_result,
            )
        except FileNotFoundError:
            _http_error(404, "not_found", "Conversación no encontrada")
            raise

        return envelope({**out, "msg_id": msg_id}, warnings=warnings)


@router.get("/conversations/{conv_id}/messages/{msg_id}/attachments/{filename}")
def download_attachment(conv_id: str, msg_id: str, filename: str):
    if any(x in (filename or "") for x in ("/", "\\", "..")):
        _http_error(400, "invalid_filename", "Nombre de adjunto no válido")
    try:
        p = chat_inbox.resolve_attachment_path(conv_id, msg_id, filename)
    except ValueError as e:
        msg = str(e)
        if msg == "invalid_conv_id":
            _http_error(400, "invalid_conv_id", "ID de conversación no válido")
        if msg == "invalid_msg_id":
            _http_error(400, "invalid_msg_id", "ID de mensaje no válido")
        _log.warning("download_attachment ValueError: %s", e)
        _http_error(400, "bad_request", "Solicitud no válida")
        raise
    if not p.is_file():
        _http_error(404, "not_found", "Adjunto no encontrado")
        raise
    return FileResponse(path=str(p), filename=p.name)
