"""Fixtures compartidos JMC."""

from __future__ import annotations

import os

import pytest


def pytest_configure(config):
    os.environ["JMC_TESTING"] = "1"


@pytest.fixture(autouse=True)
def _clear_cost_cache_between_tests():
    """Evita que el caché global de cost_report afecte el orden de ejecución de tests."""
    from app.services import cost_report as cr

    cr._CACHE.clear()
    cr._INFLIGHT.clear()
    yield
    cr._CACHE.clear()
    cr._INFLIGHT.clear()


@pytest.fixture(autouse=True)
def _reset_auth_lockout_between_tests():
    """Evita que el lockout por IP de Bearer contamine otros tests."""
    from app import security as sec

    with sec._AUTH_LOCK:
        sec._auth_failures.clear()
        sec._auth_locked_until.clear()
        sec._inbound_failures.clear()
        sec._inbound_locked_until.clear()
    yield
    with sec._AUTH_LOCK:
        sec._auth_failures.clear()
        sec._auth_locked_until.clear()
        sec._inbound_failures.clear()
        sec._inbound_locked_until.clear()
