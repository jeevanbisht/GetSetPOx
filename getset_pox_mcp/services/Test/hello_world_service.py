"""
HelloWorld service implementation.

This service provides a simple greeting tool that demonstrates
basic MCP tool functionality.
"""

from typing import Any
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)

async def hello_world(name: str = "World") -> dict[str, Any]:
    """
    Generate a personalized greeting message.
    
    This is a simple example tool that demonstrates how to create
    MCP tools with parameters and return structured data.
    
    Args:
        name: The name to include in the greeting (default: "World")
    
    Returns:
        A dictionary containing the greeting message and metadata.
    
    Example:
        >>> await hello_world("Alice")
        {
            "message": "Hello, Alice! Welcome to getset-pox-mcp.",
            "name": "Alice",
            "service": "hello_world"
        }
    """
    logger.info(f"HelloWorld service called with name: {name}")
    
    # Input validation
    if not name or not isinstance(name, str):
        logger.warning(f"Invalid name parameter: {name}")
        name = "World"
    
    # Sanitize input
    name = name.strip()
    if not name:
        name = "World"
    
    # Generate response
    message = f"Hello, {name}! Welcome to getset-pox-mcp."
    
    logger.debug(f"Generated greeting: {message}")
    
    return {
        "message": message,
        "name": name,
        "service": "hello_world",
    }
