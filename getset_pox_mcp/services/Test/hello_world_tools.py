"""
HelloWorld MCP tools registration.

This module defines the MCP tool schemas and handlers for the HelloWorld service.
"""

from mcp.types import Tool

def get_hello_world_tool() -> Tool:
    """
    Get the MCP Tool definition for hello_world.
    
    Returns:
        Tool object with schema definition.
    """
    return Tool(
        name="hello_world",
        description="Generate a personalized greeting message",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name to include in the greeting",
                    "default": "World",
                }
            },
            "required": [],
        },
    )
