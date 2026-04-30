"""Tests de helpers de seguridad (allowed_path, etc.)."""

from __future__ import annotations

from pathlib import Path

from app.security import allowed_path, sanitize_obj


def test_allowed_path_accepts_second_root(tmp_path):
    """Regresión: el bucle debe probar todas las raíces, no solo la primera."""
    root_a = tmp_path / "repo"
    root_b = tmp_path / "state_out"
    root_a.mkdir()
    root_b.mkdir()
    f = root_b / "x.json"
    f.write_text("{}", encoding="utf-8")
    assert allowed_path(f, (root_a, root_b)) is True


def test_allowed_path_rejects_outside(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    outsider = tmp_path / "evil" / "x.json"
    outsider.parent.mkdir(parents=True)
    outsider.write_text("{}", encoding="utf-8")
    assert allowed_path(outsider, (root,)) is False


def test_sanitize_obj_redacts_nested_keys():
    raw = {
        "ok": 1,
        "api_key": "secret",
        "nested": {"password": "x", "list": [{"bearerToken": "t"}]},
    }
    out = sanitize_obj(raw)
    assert out["ok"] == 1
    assert out["api_key"] == "[redacted]"
    assert out["nested"]["password"] == "[redacted]"
    assert out["nested"]["list"][0]["bearerToken"] == "[redacted]"
