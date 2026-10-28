from __future__ import annotations

from src.agent import build_agent


def test_agent_builds_without_calling_model():
    # We can't reliably call external LLMs in unit tests.
    # This test ensures agent wiring is valid.
    executor = build_agent(model_name="gpt-4o-mini")
    assert executor is not None

