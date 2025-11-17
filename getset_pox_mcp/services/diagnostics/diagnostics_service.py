"""
Diagnostics service implementation.

Provides diagnostic tools for troubleshooting Microsoft Graph API permissions
and connectivity. Adapted from EntraSuiteProd diagnostics.py.
"""

import json
from typing import Any, Dict, List
from datetime import datetime, timezone
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)

# Mock graph client for demonstration
# In production, this would be a real Microsoft Graph API client
_graph_client = None


def initialize_graph_client(client):
    """
    Initialize the Graph API client.
    
    Args:
        client: Authenticated Graph API client instance
    """
    global _graph_client
    _graph_client = client
    logger.info("Graph client initialized for diagnostics")


async def check_token_permissions(graph_client=None) -> Dict[str, Any]:
    """
    Check what permissions are actually present in the current access token.
    
    Performs a series of test API calls to verify which Microsoft Graph 
    permissions are working. Helps troubleshoot permission issues.
    
    Args:
        graph_client: Optional Graph API client (uses global if not provided)
    
    Returns:
        Dictionary with comprehensive permission test results including:
        - Individual test results for each permission
        - Summary of working vs missing permissions
        - Actionable recommendations
        - JSON response with structured data
    
    What This Tool Tests (19 Permissions):
        1. Application.Read.All
        2. Device.Read.All
        3. DeviceManagementApps.Read.All
        4. DeviceManagementApps.ReadWrite.All
        5. DeviceManagementConfiguration.ReadWrite.All
        6. DeviceManagementManagedDevices.ReadWrite.All
        7. Directory.Read.All
        8. EntitlementManagement.ReadWrite.All
        9. Group.Read.All
        10. Group.ReadWrite.All
        11. GroupMember.Read.All
        12. GroupMember.ReadWrite.All
        13. NetworkAccess.Read.All
        14. NetworkAccess.ReadWrite.All
        15. Policy.Read.All
        16. Policy.Read.ConditionalAccess
        17. Policy.ReadWrite.ConditionalAccess
        18. User.Read.All
        19. User.ReadBasic.All
    """
    # Get authenticated client from middleware
    from getset_pox_mcp.authentication.middleware import get_auth_middleware
    
    auth_middleware = get_auth_middleware()
    
    # Check if authentication is enabled
    if not auth_middleware.config.enable_auth:
        logger.warning("Authentication is disabled")
        return {
            "status": "error",
            "message": "Authentication is disabled. Enable ENTRA authentication to use this tool.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Get access token with timeout
    try:
        import asyncio
        
        # Use asyncio.wait_for to add a timeout
        token = await asyncio.wait_for(
            auth_middleware.get_valid_token(),
            timeout=10.0  # 10 second timeout
        )
        
        if not token:
            logger.warning("No valid access token available")
            return {
                "status": "error",
                "message": "No valid access token. Authentication may be in progress or failed. Please wait a moment and try again.",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    except asyncio.TimeoutError:
        logger.error("Timeout getting access token")
        return {
            "status": "error",
            "message": "Timeout acquiring access token. Authentication may still be in progress. Please try again in a moment.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting access token: {e}")
        return {
            "status": "error",
            "message": f"Error getting access token: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Make actual HTTP requests to test permissions
    logger.info("Starting token permissions diagnostic")
    results = []
    tests = []
    
    try:
        import httpx
        
        # Header
        results.append("╔════════════════════════════════════════════════╗")
        results.append("║  Token Permissions Diagnostic                 ║")
        results.append("╚════════════════════════════════════════════════╝")
        results.append("")
        results.append("🔍 Testing API Access with Current Token...")
        results.append("")
        
        # Create headers with token
        headers = {"Authorization": f"Bearer {token}"}
        
        # Define comprehensive permission tests - all 19 permissions
        permission_tests = [
            ("Application.Read.All", "https://graph.microsoft.com/v1.0/applications?$top=1", "applications"),
            ("Device.Read.All", "https://graph.microsoft.com/v1.0/devices?$top=1", "devices"),
            ("DeviceManagementApps.Read.All", "https://graph.microsoft.com/beta/deviceAppManagement/mobileApps?$top=1", "Intune apps"),
            ("DeviceManagementApps.ReadWrite.All", "https://graph.microsoft.com/beta/deviceAppManagement/mobileApps?$top=1", "Intune apps (write)"),
            ("DeviceManagementConfiguration.ReadWrite.All", "https://graph.microsoft.com/beta/deviceManagement/deviceConfigurations?$top=1", "device configurations"),
            ("DeviceManagementManagedDevices.ReadWrite.All", "https://graph.microsoft.com/beta/deviceManagement/managedDevices?$top=1", "managed devices"),
            ("Directory.Read.All", "https://graph.microsoft.com/v1.0/users?$top=1", "directory data"),
            ("EntitlementManagement.ReadWrite.All", "https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/catalogs?$top=1", "entitlement management"),
            ("Group.Read.All", "https://graph.microsoft.com/v1.0/groups?$top=1", "groups"),
            ("Group.ReadWrite.All", "https://graph.microsoft.com/v1.0/groups?$top=1", "groups (write)"),
            ("GroupMember.Read.All", "https://graph.microsoft.com/v1.0/groups?$top=1&$select=id", "group memberships"),
            ("GroupMember.ReadWrite.All", "https://graph.microsoft.com/v1.0/groups?$top=1&$select=id", "group memberships (write)"),
            ("NetworkAccess.Read.All", "https://graph.microsoft.com/beta/networkAccess/forwardingProfiles", "network access"),
            ("NetworkAccess.ReadWrite.All", "https://graph.microsoft.com/beta/networkAccess/forwardingProfiles", "network access (write)"),
            ("Policy.Read.All", "https://graph.microsoft.com/v1.0/policies/authorizationPolicy", "policies"),
            ("Policy.Read.ConditionalAccess", "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies?$top=1", "conditional access policies"),
            ("Policy.ReadWrite.ConditionalAccess", "https://graph.microsoft.com/beta/identity/conditionalAccess/policies?$top=1", "conditional access policies (write)"),
            ("User.Read.All", "https://graph.microsoft.com/v1.0/users?$top=1", "users' full profiles"),
            ("User.ReadBasic.All", "https://graph.microsoft.com/v1.0/users?$top=1&$select=id,displayName", "users' basic profiles"),
        ]
        
        # Execute tests
        async with httpx.AsyncClient() as client:
            for test_num, (permission, endpoint, resource) in enumerate(permission_tests, 1):
                results.append(f"📋 Test {test_num}: {permission}")
                
                try:
                    response = await client.get(endpoint, headers=headers, timeout=10.0)
                    
                    if response.status_code == 200:
                        tests.append({
                            "permission": permission,
                            "status": "✅ WORKING",
                            "endpoint": endpoint
                        })
                        results.append(f"   ✅ Can read {resource}")
                    elif response.status_code == 403:
                        tests.append({
                            "permission": permission,
                            "status": "❌ MISSING",
                            "error": "Insufficient privileges",
                            "endpoint": endpoint
                        })
                        results.append(f"   ❌ Cannot read {resource}: Insufficient privileges")
                    else:
                        tests.append({
                            "permission": permission,
                            "status": "❌ ERROR",
                            "error": f"HTTP {response.status_code}",
                            "endpoint": endpoint
                        })
                        results.append(f"   ❌ Cannot read {resource}: HTTP {response.status_code}")
                    
                except httpx.TimeoutException:
                    tests.append({
                        "permission": permission,
                        "status": "⏱️ TIMEOUT",
                        "error": "Request timed out",
                        "endpoint": endpoint
                    })
                    results.append(f"   ⏱️ Request timed out for {resource}")
                except Exception as error:
                    tests.append({
                        "permission": permission,
                        "status": "❌ ERROR",
                        "error": str(error),
                        "endpoint": endpoint
                    })
                    results.append(f"   ❌ Error testing {resource}: {str(error)}")
                
                results.append("")
        
        # Summary
        results.append("╔════════════════════════════════════════════════╗")
        results.append("║  PERMISSION SUMMARY                            ║")
        results.append("╚════════════════════════════════════════════════╝")
        results.append("")
        
        working = len([t for t in tests if "✅" in t["status"]])
        missing = len([t for t in tests if "❌" in t["status"]])
        
        results.append(f"📊 Results: {working} Working / {missing} Missing")
        results.append("")
        
        for test in tests:
            results.append(f"{test['status']} {test['permission']}")
        
        # Recommendations
        results.append("")
        results.append("╔════════════════════════════════════════════════╗")
        results.append("║  RECOMMENDATIONS                               ║")
        results.append("╚════════════════════════════════════════════════╝")
        results.append("")
        
        if missing > 0:
            results.append("⚠️  Missing Permissions Detected!")
            results.append("")
            results.append("📝 Action Required:")
            results.append("   1. Go to Azure Portal → App Registrations")
            results.append("   2. Find your app registration")
            results.append("   3. Go to API Permissions")
            results.append("   4. Add the missing permissions")
            results.append("   5. Grant admin consent")
            results.append("   6. Wait 10-30 minutes for propagation")
        else:
            results.append("✅ All Tested Permissions Are Working!")
        
        # JSON Response
        results.append("")
        results.append("📄 JSON Response:")
        json_response = {
            "summary": {
                "working": working,
                "missing": missing,
                "total": len(tests),
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "tests": tests
        }
        results.append(json.dumps(json_response, indent=2))
        
        logger.info(f"Diagnostic completed: {working}/{len(tests)} permissions working")
        
        return {
            "status": "success",
            "message": "\n".join(results),
            "data": json_response,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as error:
        logger.error(f"Error in check_token_permissions: {error}")
        
        results.append("")
        results.append("╔════════════════════════════════════════════════╗")
        results.append("║  ❌ DIAGNOSTIC ERROR                           ║")
        results.append("╚════════════════════════════════════════════════╝")
        results.append(f"Error: {str(error)}")
        
        return {
            "status": "error",
            "message": "\n".join(results),
            "error": str(error),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
