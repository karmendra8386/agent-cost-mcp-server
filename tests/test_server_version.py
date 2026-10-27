"""The MCP initialize handshake must report the package version,
not the MCP SDK's version."""

from agent_cost_mcp_server import __version__
from agent_cost_mcp_server.server import mcp


def test_server_info_version_is_package_version():
    options = mcp._mcp_server.create_initialization_options()
    assert options.server_name == "agent-cost-mcp-server"
    assert options.server_version == __version__
