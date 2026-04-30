"""GET /v1/skills/coverage."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.skills_coverage import build_skills_coverage
from app.util_response import envelope

router = APIRouter(prefix="/skills", dependencies=[Depends(require_token)])


@router.get("/coverage")
def skills_coverage():
    return envelope(build_skills_coverage())
