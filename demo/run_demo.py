"""Reproduce the agent-cost demo: a real MCP client session.

Connects to this repo's server over stdio with the official `mcp` SDK
(the version this package pins, mcp<2 — install with `pip install -e .`),
lists its tools, and calls each one with a worked example:

  price_usage -> estimate_run_cost -> compare_models_for_task
  -> record_spend x2 -> budget_status

The ledger is written to demo/ledger.json (via AGENT_COST_LEDGER_PATH)
and the full session printed to demo/session-output.txt.

    python demo/run_demo.py
"""
import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
LEDGER = HERE / "ledger.json"


def show(label, result):
    payload = None
    if getattr(result, "structuredContent", None):
        payload = result.structuredContent
    else:
        for c in result.content:
            if getattr(c, "type", None) == "text":
                try:
                    payload = json.loads(c.text)
                except Exception:
                    payload = c.text
    print(f"\n>> {label}")
    print(json.dumps(payload, indent=1)[:1800])
    return payload


async def main():
    if LEDGER.exists():
        LEDGER.unlink()
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "agent_cost_mcp_server.server"],
        env={**os.environ, "PYTHONPATH": str(SRC),
             "AGENT_COST_LEDGER_PATH": str(LEDGER)},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(">> tools/list — server offers:")
            for t in tools.tools:
                print(f"   - {t.name}")
            show("price_usage: Sonnet 4.5, 12,000 in / 1,800 out",
                 await session.call_tool("price_usage", {
                     "model_id": "anthropic.claude-sonnet-4-5",
                     "input_tokens": 12000, "output_tokens": 1800}))
            show("estimate_run_cost: same workload, every model",
                 await session.call_tool("estimate_run_cost", {
                     "model_id": "anthropic.claude-sonnet-4-5",
                     "input_tokens": 12000, "output_tokens": 1800}))
            show("compare_models_for_task: cost per SUCCESSFUL task "
                 "(Haiku succeeds 60%, Sonnet 92%, Opus 97%)",
                 await session.call_tool("compare_models_for_task", {
                     "input_tokens": 12000, "output_tokens": 1800,
                     "success_rates": {
                         "anthropic.claude-haiku-4-5": 0.60,
                         "anthropic.claude-sonnet-4-5": 0.92,
                         "anthropic.claude-opus-4-5": 0.97}}))
            show("record_spend #1: task demo-task, Sonnet run",
                 await session.call_tool("record_spend", {
                     "task_id": "demo-task",
                     "model_id": "anthropic.claude-sonnet-4-5",
                     "input_tokens": 12000, "output_tokens": 1800}))
            show("record_spend #2: task demo-task, Haiku retry",
                 await session.call_tool("record_spend", {
                     "task_id": "demo-task",
                     "model_id": "anthropic.claude-haiku-4-5",
                     "input_tokens": 9400, "output_tokens": 1200}))
            show("budget_status: demo-task against a $0.10 budget",
                 await session.call_tool("budget_status", {
                     "task_id": "demo-task", "budget_usd": 0.10}))


if __name__ == "__main__":
    asyncio.run(main())
