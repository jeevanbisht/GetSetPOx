"""
Tests for the diagnostics service.
"""

import pytest
from getset_pox_mcp.services.diagnostics.diagnostics_service import check_token_permissions

@pytest.mark.asyncio
async def test_check_token_permissions_no_client():
    """Test check_token_permissions with no Graph client."""
    result = await check_token_permissions()
    
    assert "status" in result
    assert "message" in result
    assert "timestamp" in result
    assert result["status"] == "error"
    assert "Graph client not initialized" in result["message"]

@pytest.mark.asyncio
async def test_check_token_permissions_with_mock_client():
    """Test check_token_permissions with a mock Graph client."""
    # Mock Graph client (in production, use actual client)
    mock_client = type('MockClient', (), {'get': lambda self, url: None})()
    
    result = await check_token_permissions(graph_client=mock_client)
    
    assert "status" in result
    assert "message" in result
    assert "data" in result
    assert "timestamp" in result
    assert result["status"] == "success"
    
    # Check data structure
    data = result["data"]
    assert "summary" in data
    assert "tests" in data
    assert data["summary"]["total"] == 5  # 5 permission tests
    
@pytest.mark.asyncio
async def test_check_token_permissions_message_format():
    """Test that check_token_permissions returns properly formatted message."""
    mock_client = type('MockClient', (), {'get': lambda self, url: None})()
    
    result = await check_token_permissions(graph_client=mock_client)
    
    assert "message" in result
    message = result["message"]
    
    # Check for expected sections
    assert "Token Permissions Diagnostic" in message
    assert "PERMISSION SUMMARY" in message
    assert "RECOMMENDATIONS" in message
    assert "JSON Response" in message
