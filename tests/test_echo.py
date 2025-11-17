"""
Tests for the Echo service.
"""

import pytest
from getset_pox_mcp.services.Test.echo_service import echo

@pytest.mark.asyncio
async def test_echo_basic():
    """Test echo with basic message."""
    result = await echo(message="Hello World")
    
    assert "original" in result
    assert "echoed" in result
    assert "uppercase" in result
    assert "timestamp" in result
    assert "length" in result
    assert "service" in result
    
    assert result["original"] == "Hello World"
    assert result["echoed"] == "Hello World"
    assert result["uppercase"] is False
    assert result["length"] == 11
    assert result["service"] == "echo"

@pytest.mark.asyncio
async def test_echo_uppercase():
    """Test echo with uppercase flag."""
    result = await echo(message="hello", uppercase=True)
    
    assert result["original"] == "hello"
    assert result["echoed"] == "HELLO"
    assert result["uppercase"] is True
    assert result["length"] == 5

@pytest.mark.asyncio
async def test_echo_lowercase_flag():
    """Test echo with explicit lowercase flag."""
    result = await echo(message="HELLO", uppercase=False)
    
    assert result["original"] == "HELLO"
    assert result["echoed"] == "HELLO"
    assert result["uppercase"] is False

@pytest.mark.asyncio
async def test_echo_empty_message():
    """Test echo with empty message raises ValueError."""
    with pytest.raises(ValueError, match="non-empty string"):
        await echo(message="")

@pytest.mark.asyncio
async def test_echo_special_characters():
    """Test echo with special characters."""
    message = "Hello! @#$%^&*()"
    result = await echo(message=message)
    
    assert result["original"] == message
    assert result["echoed"] == message
    assert result["length"] == len(message)

@pytest.mark.asyncio
async def test_echo_unicode():
    """Test echo with unicode characters."""
    message = "Hello 世界 🌍"
    result = await echo(message=message)
    
    assert result["original"] == message
    assert result["echoed"] == message

@pytest.mark.asyncio
async def test_echo_multiline():
    """Test echo with multiline message."""
    message = "Line 1\nLine 2\nLine 3"
    result = await echo(message=message)
    
    assert result["original"] == message
    assert result["echoed"] == message
    assert result["length"] == len(message)

@pytest.mark.asyncio
async def test_echo_timestamp_format():
    """Test that echo returns properly formatted timestamp."""
    result = await echo(message="test")
    
    # Check timestamp is in ISO format with Z suffix
    assert "timestamp" in result
    assert result["timestamp"].endswith("Z")
    assert "T" in result["timestamp"]
