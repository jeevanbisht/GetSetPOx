"""
Echo service implementation.

This service provides an echo tool that returns the input message
along with metadata, demonstrating parameter handling and structured responses.
"""

from datetime import datetime, timezone
from typing import Any
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)

async def echo(message: str, uppercase: bool = False) -> dict[str, Any]:
    """
    Echo back the provided message with metadata.
    
    This tool demonstrates handling multiple parameters with different types
    and returning structured data with computed fields.
    
    Args:
        message: The message to echo back
        uppercase: If True, return the message in uppercase (default: False)
    
    Returns:
        A dictionary containing the original message, echoed message,
        timestamp, and other metadata.
    
    Raises:
        ValueError: If message is empty or invalid.
    
    Example:
        >>> await echo("Hello World", uppercase=True)
        {
            "original": "Hello World",
            "echoed": "HELLO WORLD",
            "uppercase": True,
            "timestamp": "2025-01-16T19:42:00.000Z",
            "length": 11,
            "service": "echo"
        }
    """
    logger.info(f"Echo service called with message: '{message}', uppercase: {uppercase}")
    
    # Input validation
    if not message or not isinstance(message, str):
        error_msg = "Message parameter must be a non-empty string"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Process message
    echoed_message = message.upper() if uppercase else message
    
    # Generate timestamp
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    # Calculate message length
    message_length = len(message)
    
    logger.debug(f"Processed echo: original='{message}', echoed='{echoed_message}'")
    
    return {
        "original": message,
        "echoed": echoed_message,
        "uppercase": uppercase,
        "timestamp": timestamp,
        "length": message_length,
        "service": "echo",
    }
