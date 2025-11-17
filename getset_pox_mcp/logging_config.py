"""
Logging configuration for the getset-pox-mcp server.

This module sets up structured logging with appropriate formatters
and handlers based on the server configuration.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Configure logging for the MCP server.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, logs only to stderr.
    
    Returns:
        Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger("getset_pox_mcp")
    logger.setLevel(getattr(logging, log_level))
    
    # Remove any existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler (stderr to avoid interfering with STDIO transport)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(getattr(logging, log_level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str = "getset_pox_mcp") -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name.
    
    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
