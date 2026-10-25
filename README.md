# Agent Cost MCP Server

An MCP server that gives agents and developers tools to **estimate, budget,
and compare the cost of LLM work before and during a run** — the model-spend
counterpart to AWS infrastructure cost tooling.

Agent frameworks decide for themselves how many model calls a task takes, so
the cost of a run is usually only visible after the bill arrives. This server
answers, from inside your tooling:

- *What will this task cost on model A vs model B?*
- *Which model is cheapest per **successful** task, not per token?*
- *Has this run already burned its budget?*

The server is self-contained: a maintained pricing snapshot ships with it,
no AWS account or API key is needed, all state is a local JSON ledger, and
it makes no network calls at runtime.

## Tools

| Tool | Arguments | Returns |
| --- | --- | --- |
| `price_usage` | `model_id`, `input_tokens`, `output_tokens` | Input/output/total cost in USD for one concrete usage record |
| `estimate_run_cost` | `model_id`, `input_tokens`, `output_tokens` | The model's cost for one run, plus the same workload priced on every other model, cheapest first |
| `compare_models_for_task` | `input_tokens`, `output_tokens`, `success_rates?` | All models ranked by expected **cost per successful task** (cost per attempt ÷ success rate) |
| `record_spend` | `task_id`, `model_id`, `input_tokens`, `output_tokens` | The recorded ledger entry, priced at list rates |
| `budget_status` | `task_id`, `budget_usd` | `{spent_usd, remaining_usd, over_budget, calls, models_used, by_model}` for the task. `by_model` maps each model_id to `{calls, input_tokens, output_tokens, spent_usd}` |

Cost per token is the wrong ranking for agent work: a cheap model that
fails half its tasks costs more per success than a pricier, reliable one.
Pass measured success rates to `compare_models_for_task` if you have them;
models without a supplied rate are ranked on raw cost.

This server supplies the numbers. *Enforcing* a budget (stopping a run)
belongs to the agent framework — see
[BudgetedModel in strands-agents/samples](https://github.com/strands-agents/samples)
for that pattern.

## Installation

Run it with `uvx`:

```json
{
  "mcpServers": {
    "agent-cost": {
      "command": "uvx",
      "args": ["agent-cost-mcp-server"]
    }
  }
}
```

Or install with pip:

```bash
pip install agent-cost-mcp-server
agent-cost-mcp-server
```

## Pricing snapshot

Prices live in `src/agent_cost_mcp_server/pricing.json` — a versioned
snapshot of list prices (USD per 1M tokens) for major Bedrock and
OpenAI-compatible models, dated in the file. Prices change; verify against
the provider's pricing page before making spending decisions. Updating the
snapshot is a one-file change, and the server reads it at startup.

## Ledger

`record_spend` appends to a local JSON ledger at
`~/.agent-cost-mcp-server/ledger.json`. Set `AGENT_COST_LEDGER_PATH` to use
a different file. Nothing leaves the machine.

## Background

The pricing and cost-per-success model are a port of
[tokenecon](https://pypi.org/project/tokenecon/), an open-source library
for per-task agent cost accounting (paper:
[doi.org/10.5281/zenodo.23195511](https://doi.org/10.5281/zenodo.23195511)),
including a Strands integration that prices live agent runs. This server
exposes the same math over MCP so any agent or IDE can call it.

Proposed for the [awslabs/mcp](https://github.com/awslabs/mcp) collection
in [RFC #4772](https://github.com/awslabs/mcp/issues/4772).

## Development

```bash
uv sync --extra dev   # or: pip install -e ".[dev]"
pytest
```

## Cite

If you use this software in your work, please cite the software itself.

**Software**

```bibtex
@software{pandey_agent_cost_mcp_server_2026,
  author = {Pandey, Karmendra},
  title = {agent-cost-mcp-server},
  version = {0.1.0},
  url = {https://github.com/karmendra8386/agent-cost-mcp-server},
  date = {2026-10-20}
}
```

The cost model is described in the companion preprint: Pandey, K., "Token-Economics for Agentic AI: A Cost Model and Tiered Routing Reference" — doi:10.5281/zenodo.23195511.

A `CITATION.cff` is included for automated citation tooling.

## License

Apache-2.0 — see [LICENSE](LICENSE).

Copyright 2026 Karmendra Pandey.
