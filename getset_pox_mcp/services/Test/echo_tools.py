"""
Echo MCP tools registration.

This module defines the MCP tool schemas and handlers for the Echo service.
"""

from mcp.types import Tool

def get_echo_tool() -> Tool:
    """
    Get the MCP Tool definition for echo.
    
    Returns:
        Tool object with schema definition.
    """
    return Tool(
        name="echo",
        description="Echo back the provided message with metadata",
        inputSchema={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to echo back",
                },
                "uppercase": {
                    "type": "boolean",
                    "description": "If true, return the message in uppercase",
                    "default": False,
                },
            },
            "required": ["message"],
        },
    )
