"""
Test service package.

This package contains example services demonstrating MCP tool implementations
using the _service.py and _tools.py pattern.
"""

from getset_pox_mcp.services.Test.hello_world_service import hello_world
from getset_pox_mcp.services.Test.echo_service import echo

__all__ = ["hello_world", "echo"]
