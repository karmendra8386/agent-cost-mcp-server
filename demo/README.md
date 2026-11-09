# agent-cost-mcp-server demo

`demo.gif` (top of the repo README) renders a live MCP client session run
on Nov 9, 2026: a client using the official `mcp` SDK connected over stdio
to the server in this repo, listed its five tools, and called each one.
The full record is here:

| File | What it is |
|---|---|
| `session-output.txt` | The complete session: every tool call and its full JSON response. Headline numbers: `price_usage` prices a 12,000-in / 1,800-out Sonnet 4.5 run at **$0.063**; `compare_models_for_task` re-ranks models by **cost per successful task** (cost per attempt ÷ success rate) rather than cost per token; two `record_spend` calls ($0.063 Sonnet + $0.0154 Haiku) leave `budget_status` at **$0.0784 spent of a $0.10 budget, $0.0216 remaining**. |
| `ledger.json` | The actual ledger file the server wrote during the run (redirected here with `AGENT_COST_LEDGER_PATH`). |
| `run_demo.py` | The client that produced the session. Run it in an environment with this package's dependencies installed (`pip install -e .` — note the package pins `mcp<2`). |

The GIF is a text rendering of the captured session output in
`session-output.txt` — the numbers in it are the server's own responses.
