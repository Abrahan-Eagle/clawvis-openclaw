"""FastAPI JMC — mayormente lectura local; escritura acotada a modo (POST /v1/modes/current). Bind 127.0.0.1."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.config import get_cors_origins
from app.routers import (
    chat,
    costs,
    diagnostics,
    docs_lint,
    dossiers,
    escalations,
    external,
    files,
    gates,
    heartbeats,
    health,
    inbound,
    judge,
    last30days,
    memory,
    modes,
    openclaw,
    public_v110,
    runtime,
    search,
    skills,
    state,
    system,
    webhooks,
)

_log = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault(
            "Permissions-Policy",
            "geolocation=(), microphone=(), camera=()",
        )
        return response

# Sin límite por defecto en ejecución de tests (evita 429 al importar app tras muchos POST).
_rate = [] if os.environ.get("JMC_TESTING") == "1" else ["5/second"]
limiter = Limiter(key_func=get_remote_address, default_limits=_rate)

app = FastAPI(title="Jarvis Mission Control", version="1.0.0")
app.state.limiter = limiter
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    _log.exception("Error no manejado: %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": {"error": {"code": "internal", "message": "Internal error"}}},
    )


_cors_list = get_cors_origins()
if _cors_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(public_v110.router, prefix="/v1", tags=["public"])
app.include_router(health.router, prefix="/v1", tags=["health"])
app.include_router(openclaw.router, prefix="/v1", tags=["openclaw"])
app.include_router(state.router, prefix="/v1", tags=["state"])
app.include_router(costs.router, prefix="/v1", tags=["costs"])
app.include_router(modes.router, prefix="/v1", tags=["modes"])
app.include_router(escalations.router, prefix="/v1", tags=["escalations"])
app.include_router(dossiers.router, prefix="/v1", tags=["dossiers"])
app.include_router(gates.router, prefix="/v1", tags=["gates"])
app.include_router(judge.router, prefix="/v1", tags=["judge"])
app.include_router(last30days.router, prefix="/v1", tags=["last30days"])
app.include_router(system.router, prefix="/v1", tags=["system"])
app.include_router(runtime.router, prefix="/v1", tags=["runtime"])
app.include_router(memory.router, prefix="/v1", tags=["memory"])
app.include_router(files.router, prefix="/v1", tags=["files"])
app.include_router(search.router, prefix="/v1", tags=["search"])
app.include_router(diagnostics.router, prefix="/v1", tags=["diagnostics"])
app.include_router(external.router, prefix="/v1", tags=["external"])
app.include_router(skills.router, prefix="/v1", tags=["skills"])
app.include_router(webhooks.router, prefix="/v1", tags=["webhooks"])
app.include_router(inbound.router, prefix="/v1", tags=["webhooks-inbound"])
app.include_router(docs_lint.router, prefix="/v1", tags=["docs"])
app.include_router(heartbeats.router, prefix="/v1", tags=["heartbeats"])
app.include_router(chat.router, prefix="/v1", tags=["chat"])

# jmc/ui junto a jmc/adapter
_UI_DIR = Path(__file__).resolve().parents[2] / "ui"
if _UI_DIR.is_dir():
    app.mount("/ui", StaticFiles(directory=str(_UI_DIR), html=True), name="ui")


@app.get("/")
def root():
    return {"service": "jmc-adapter", "ui": "/ui/", "api": "/v1/health"}
