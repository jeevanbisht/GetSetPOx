"""
POC Tools MCP registration.

This module defines the MCP tool schemas for the POC service.
"""

from mcp.types import Tool

def get_GovernInternetAccessPOC_tool() -> Tool:
    """Get the MCP Tool definition for GovernInternetAccessPOC."""
    return Tool(
        name="GovernInternetAccessPOC",
        description="Creates an Internet Access governance user group, access catalog, and access package for the POC workflow. Automatically initializes a complete 'Internet Access Governance' flow for POC users with retry logic and async operation support.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )
