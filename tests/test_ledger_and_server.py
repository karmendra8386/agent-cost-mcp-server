import asyncio

from agent_cost_mcp_server.ledger import Ledger
from agent_cost_mcp_server.server import mcp


def test_record_and_status(tmp_path):
    ledger = Ledger(path=tmp_path / "ledger.json")
    ledger.record("task-1", "anthropic.claude-haiku-4-5", 1_000_000, 0, 1.0)
    ledger.record("task-1", "anthropic.claude-haiku-4-5", 0, 1_000_000, 5.0)
    ledger.record("task-2", "openai.gpt-5-mini", 100, 100, 0.01)

    status = ledger.status("task-1", budget_usd=10.0)
    assert status["spent_usd"] == 6.0
    assert status["remaining_usd"] == 4.0
    assert status["calls"] == 2
    assert status["over_budget"] is False
    assert status["models_used"] == ["anthropic.claude-haiku-4-5"]


def test_over_budget_and_unknown_task(tmp_path):
    ledger = Ledger(path=tmp_path / "ledger.json")
    ledger.record("task-1", "openai.gpt-5", 1_000_000, 1_000_000, 11.25)
    assert ledger.status("task-1", budget_usd=10.0)["over_budget"] is True

    empty = ledger.status("never-seen", budget_usd=5.0)
    assert empty["spent_usd"] == 0
    assert empty["calls"] == 0


def test_all_five_tools_registered():
    tools = asyncio.run(mcp.list_tools())
    names = {t.name for t in tools}
    assert names == {
        "price_usage",
        "estimate_run_cost",
        "compare_models_for_task",
        "record_spend",
        "budget_status",
    }
