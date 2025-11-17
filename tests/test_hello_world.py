"""
Tests for the HelloWorld service.
"""

import pytest
from getset_pox_mcp.services.Test.hello_world_service import hello_world

@pytest.mark.asyncio
async def test_hello_world_default():
    """Test hello_world with default name parameter."""
    result = await hello_world()
    
    assert "message" in result
    assert "name" in result
    assert "service" in result
    assert result["name"] == "World"
    assert "Hello, World!" in result["message"]
    assert result["service"] == "hello_world"

@pytest.mark.asyncio
async def test_hello_world_custom_name():
    """Test hello_world with custom name."""
    result = await hello_world(name="Alice")
    
    assert result["name"] == "Alice"
    assert "Hello, Alice!" in result["message"]
    assert result["service"] == "hello_world"

@pytest.mark.asyncio
async def test_hello_world_empty_name():
    """Test hello_world with empty string falls back to default."""
    result = await hello_world(name="")
    
    assert result["name"] == "World"
    assert "Hello, World!" in result["message"]

@pytest.mark.asyncio
async def test_hello_world_whitespace_name():
    """Test hello_world with whitespace-only name falls back to default."""
    result = await hello_world(name="   ")
    
    assert result["name"] == "World"
    assert "Hello, World!" in result["message"]

@pytest.mark.asyncio
async def test_hello_world_special_characters():
    """Test hello_world with special characters in name."""
    result = await hello_world(name="José")
    
    assert result["name"] == "José"
    assert "Hello, José!" in result["message"]

@pytest.mark.asyncio
async def test_hello_world_long_name():
    """Test hello_world with a long name."""
    long_name = "A" * 100
    result = await hello_world(name=long_name)
    
    assert result["name"] == long_name
    assert long_name in result["message"]
