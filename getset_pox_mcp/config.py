"""
Configuration management for the getset-pox-mcp server.

This module handles all configuration settings from environment variables
and provides default values for the MCP server.
"""

import os
from dataclasses import dataclass
from typing import Literal


@dataclass
class ServerConfig:
    """Configuration settings for the MCP server."""

    # Transport settings
    transport: Literal["stdio", "http"] = "stdio"
    
    # HTTP transport settings
    http_host: str = "127.0.0.1"
    http_port: int = 3000
    http_path: str = "/mcp"
    stateless_http: bool = False
    
    # Logging settings
    log_level: str = "INFO"
    log_file: str | None = None
    
    @classmethod
    def from_env(cls) -> "ServerConfig":
        """
        Create configuration from environment variables.
        
        Returns:
            ServerConfig instance populated from environment variables.
        """
        transport = os.getenv("TRANSPORT", "stdio").lower()
        if transport not in ("stdio", "http"):
            raise ValueError(f"Invalid transport mode: {transport}. Must be 'stdio' or 'http'.")
        
        return cls(
            transport=transport,  # type: ignore
            http_host=os.getenv("HTTP_HOST", "127.0.0.1"),
            http_port=int(os.getenv("HTTP_PORT", "3000")),
            http_path=os.getenv("HTTP_PATH", "/mcp"),
            stateless_http=os.getenv("STATELESS_HTTP", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            log_file=os.getenv("LOG_FILE"),
        )
    
    def validate(self) -> None:
        """
        Validate configuration settings.
        
        Raises:
            ValueError: If any configuration setting is invalid.
        """
        if self.transport not in ("stdio", "http"):
            raise ValueError(f"Invalid transport: {self.transport}")
        
        if self.http_port < 1 or self.http_port > 65535:
            raise ValueError(f"Invalid HTTP port: {self.http_port}")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level not in valid_log_levels:
            raise ValueError(
                f"Invalid log level: {self.log_level}. "
                f"Must be one of: {', '.join(valid_log_levels)}"
            )
