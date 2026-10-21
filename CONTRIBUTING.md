# Contributing to agent-cost-mcp-server

Thanks for your interest in improving the agent cost MCP server.
Contributions of all sizes are welcome: pricing-snapshot updates, new
tools, ledger improvements, and documentation.

## Ground rules

- **Self-contained by design.** The server makes no network calls at
  runtime, needs no account or API key, and keeps all state in a local
  JSON ledger. Pull requests that add a runtime service dependency will
  not be accepted.
- **Pricing data carries a source.** Every price in
  `src/agent_cost_mcp_server/pricing.json` must come from the provider's
  public pricing page. A pricing PR must link that page in its
  description and bump `snapshot_version` and `snapshot_date` in the
  same change.
- **Python 3.10+**, and the MCP Python SDK is pinned to v1
  (`mcp[cli]>=1.0.0,<2.0.0`) to match the awslabs/mcp conventions this
  server is proposed under (RFC #4772).

## Reporting bugs and requesting features

Open an issue at
https://github.com/karmendra8386/agent-cost-mcp-server/issues with what
you called (tool name and arguments), what you expected, what you got,
and your Python and server versions.

## Development setup

```bash
git clone https://github.com/karmendra8386/agent-cost-mcp-server.git
cd agent-cost-mcp-server
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running the tests

```bash
python -m pytest tests/ -q
```

Tests run offline; ledger tests use a temporary file via the
`AGENT_COST_LEDGER_PATH` environment variable. New behaviour must come
with tests in the same style, and the full suite should pass before you
open a pull request.

## Pull requests

1. Fork the repository and create a topic branch.
2. Keep the change focused; unrelated refactors belong in separate PRs.
3. Add or update tests for behaviour changes, and update the README's
   tool table if you add or change a tool.
4. For tool changes, verify the math in your PR description with a worked
   example (model, token counts, expected cost).
5. In the PR description, state the problem, the change, and how you
   tested it.

Maintainer review is by the project author. Response times are
best-effort — this is a single-maintainer project.

## License

By contributing, you agree that your contributions are licensed under
the Apache License 2.0 (see `LICENSE`).
