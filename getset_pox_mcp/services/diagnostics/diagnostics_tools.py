"""
Diagnostics MCP tools registration.

This module defines the MCP tool schemas for the diagnostics service.
"""

from mcp.types import Tool

def get_check_token_permissions_tool() -> Tool:
    """
    Get the MCP Tool definition for check_token_permissions.
    
    Returns:
        Tool object with schema definition.
    """
    return Tool(
        name="check_token_permissions",
        description="Check Microsoft Graph API token permissions and troubleshoot access issues",
        inputSchema={
            "type": "object",
            "properties": {
                "graph_client": {
                    "type": ["object", "null"],
                    "description": "Optional Graph API client instance (uses global if not provided)",
                    "default": None,
                }
            },
            "required": [],
        },
    )
