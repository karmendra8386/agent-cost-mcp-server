import pytest

from agent_cost_mcp_server.pricing import (
    PricingTable,
    compare_models_for_task,
    estimate_run_cost,
    price_usage,
)

TABLE = PricingTable()


def test_price_usage_math():
    # Claude Haiku 4.5: $1.00 in / $5.00 out per 1M tokens.
    result = price_usage(TABLE, "anthropic.claude-haiku-4-5", 1_000_000, 1_000_000)
    assert result["input_cost_usd"] == 1.0
    assert result["output_cost_usd"] == 5.0
    assert result["cost_usd"] == 6.0


def test_price_usage_unknown_model():
    with pytest.raises(ValueError, match="Unknown model_id"):
        price_usage(TABLE, "nope.not-a-model", 100, 100)


def test_negative_tokens_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        price_usage(TABLE, "anthropic.claude-haiku-4-5", -1, 100)


def test_estimate_includes_sorted_alternatives():
    result = estimate_run_cost(TABLE, "anthropic.claude-sonnet-4-5", 10_000, 2_000)
    assert result["model"] == "anthropic.claude-sonnet-4-5"
    assert result["cost_usd"] == pytest.approx(0.06)
    costs = [a["cost_usd"] for a in result["alternatives"]]
    assert costs == sorted(costs)
    assert all(a["model"] != "anthropic.claude-sonnet-4-5" for a in result["alternatives"])


def test_compare_ranks_by_cost_per_success_not_per_token():
    # Haiku is 3x cheaper per run, but at a 25% success rate its expected
    # cost per success ($0.08) beats nothing — Sonnet at 100% ($0.06) wins.
    result = compare_models_for_task(
        TABLE,
        10_000,
        2_000,
        success_rates={
            "anthropic.claude-haiku-4-5": 0.25,
            "anthropic.claude-sonnet-4-5": 1.0,
        },
    )
    ranked = result["ranked"]
    sonnet = next(r for r in ranked if r["model"] == "anthropic.claude-sonnet-4-5")
    haiku = next(r for r in ranked if r["model"] == "anthropic.claude-haiku-4-5")
    assert haiku["cost_per_run_usd"] < sonnet["cost_per_run_usd"]
    assert haiku["cost_per_success_usd"] == pytest.approx(0.08)
    assert sonnet["cost_per_success_usd"] == pytest.approx(0.06)
    assert ranked.index(sonnet) < ranked.index(haiku)


def test_compare_rejects_bad_success_rate():
    with pytest.raises(ValueError, match="success rate"):
        compare_models_for_task(TABLE, 100, 100, success_rates={"x": 0})
