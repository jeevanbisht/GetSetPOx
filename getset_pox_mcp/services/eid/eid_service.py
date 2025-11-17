"""
EID (Entra ID) Service Implementation.

This service provides Microsoft Entra ID (formerly Azure AD) user and device management tools
for querying users, devices, groups, and managing group memberships via Microsoft Graph API v1.0.

Dependencies:
    - httpx: For async HTTP requests to Microsoft Graph API
    - Authentication via auth_middleware for token management
"""

from typing import Any, List, Optional
from getset_pox_mcp.logging_config import get_logger
from getset_pox_mcp.authentication.middleware import get_auth_middleware
import httpx
import json
import asyncio

logger = get_logger(__name__)


async def EID_listUsers() -> dict[str, Any]:
    """
    List all users from Microsoft Graph API v1.0.
    
    Returns:
        Dictionary containing list of users with count and status.
    """
    logger.info("EID_listUsers called")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://graph.microsoft.com/v1.0/users",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        users = data.get("value", [])
        return {
            "status": "success",
            "users": users,
            "count": len(users),
            "message": json.dumps(users, indent=2)
        }
    except Exception as error:
        logger.error(f"Error listing users: {error}")
        return {"status": "error", "message": f"Error listing users: {str(error)}"}


async def EID_getUser(user_id: str) -> dict[str, Any]:
    """
    Get a specific user by ID from Microsoft Graph API v1.0.
    
    Args:
        user_id: The ID or userPrincipalName of the user
        
    Returns:
        Dictionary containing user details or error message.
    """
    logger.info(f"EID_getUser called: user_id={user_id}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/v1.0/users/{user_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        return {
            "status": "success",
            "user": data,
            "message": json.dumps(data, indent=2)
        }
    except Exception as error:
        logger.error(f"Error getting user: {error}")
        return {"status": "error", "message": f"Error getting user: {str(error)}"}


async def EID_searchUsers(query: str, top: int = 50) -> dict[str, Any]:
    """
    Search for users in Microsoft Graph API by display name or email.
    
    Args:
        query: Search query string
        top: Maximum number of results to return (default: 50, max: 999)
        
    Returns:
        Dictionary containing list of matching users or error message.
    """
    logger.info(f"EID_searchUsers called: query={query}, top={top}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Limit top parameter
        top = max(1, min(top, 999))
        
        # Search users using filter
        filter_query = f"startswith(displayName,'{query}') or startswith(userPrincipalName,'{query}')"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/v1.0/users?$filter={filter_query}&$select=id,displayName,mail,userPrincipalName&$top={top}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        users = data.get("value", [])
        return {
            "status": "success",
            "users": users,
            "count": len(users),
            "query": query,
            "message": json.dumps(users, indent=2)
        }
    except Exception as error:
        logger.error(f"Error searching users: {error}")
        return {"status": "error", "message": f"Error searching users: {str(error)}"}


async def EID_listDevices() -> dict[str, Any]:
    """
    List all devices including Entra Joined, Entra Hybrid Joined, Registered, and Compliant Devices.
    
    Returns:
        Dictionary containing list of devices with count and status.
    """
    logger.info("EID_listDevices called")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://graph.microsoft.com/v1.0/devices",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        devices = data.get("value", [])
        return {
            "status": "success",
            "devices": devices,
            "count": len(devices),
            "message": json.dumps(devices, indent=2)
        }
    except Exception as error:
        logger.error(f"Error listing devices: {error}")
        return {"status": "error", "message": f"Error listing devices: {str(error)}"}


async def EID_getDevice(device_id: str) -> dict[str, Any]:
    """
    Get a specific device by ID from Microsoft Graph API v1.0.
    
    Args:
        device_id: The ID of the device
        
    Returns:
        Dictionary containing device details or error message.
    """
    logger.info(f"EID_getDevice called: device_id={device_id}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/v1.0/devices/{device_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        return {
            "status": "success",
            "device": data,
            "message": json.dumps(data, indent=2)
        }
    except Exception as error:
        logger.error(f"Error getting device: {error}")
        return {"status": "error", "message": f"Error getting device: {str(error)}"}


async def EID_getGroups(top: int = 100) -> dict[str, Any]:
    """
    List all groups from Microsoft Graph API v1.0.
    
    Args:
        top: Maximum number of groups to return (default: 100, max: 999)
        
    Returns:
        Dictionary containing list of groups or error message.
    """
    logger.info(f"EID_getGroups called: top={top}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Limit top parameter
        top = max(1, min(top, 999))
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/v1.0/groups?$select=id,displayName,mail,description,groupTypes&$top={top}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        groups = data.get("value", [])
        return {
            "status": "success",
            "groups": groups,
            "count": len(groups),
            "nextLink": data.get("@odata.nextLink"),
            "message": json.dumps(groups, indent=2)
        }
    except Exception as error:
        logger.error(f"Error listing groups: {error}")
        return {"status": "error", "message": f"Error listing groups: {str(error)}"}


async def EID_getGroup(group_id: str) -> dict[str, Any]:
    """
    Get a specific group by ID from Microsoft Graph API v1.0.
    
    Args:
        group_id: The ID of the group
        
    Returns:
        Dictionary containing group details or error message.
    """
    logger.info(f"EID_getGroup called: group_id={group_id}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/v1.0/groups/{group_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        return {
            "status": "success",
            "group": data,
            "message": json.dumps(data, indent=2)
        }
    except Exception as error:
        logger.error(f"Error getting group: {error}")
        return {"status": "error", "message": f"Error getting group: {str(error)}"}


async def EID_getGroupMembers(group_id: str, top: int = 100) -> dict[str, Any]:
    """
    Get members of a specific group from Microsoft Graph API v1.0.
    
    Args:
        group_id: The ID of the group
        top: Maximum number of members to return (default: 100, max: 999)
        
    Returns:
        Dictionary containing list of group members or error message.
    """
    logger.info(f"EID_getGroupMembers called: group_id={group_id}, top={top}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Limit top parameter
        top = max(1, min(top, 999))
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$select=id,displayName,mail,userPrincipalName&$top={top}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        members = data.get("value", [])
        return {
            "status": "success",
            "members": members,
            "count": len(members),
            "group_id": group_id,
            "nextLink": data.get("@odata.nextLink"),
            "message": json.dumps(members, indent=2)
        }
    except Exception as error:
        logger.error(f"Error getting group members: {error}")
        return {"status": "error", "message": f"Error getting group members: {str(error)}"}


async def EID_searchGroups(query: str, top: int = 50) -> dict[str, Any]:
    """
    Search for groups in Microsoft Graph API by display name.
    
    Args:
        query: Search query string
        top: Maximum number of results to return (default: 50, max: 999)
        
    Returns:
        Dictionary containing list of matching groups or error message.
    """
    logger.info(f"EID_searchGroups called: query={query}, top={top}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Limit top parameter
        top = max(1, min(top, 999))
        
        # Search groups using filter
        filter_query = f"startswith(displayName,'{query}')"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/v1.0/groups?$filter={filter_query}&$select=id,displayName,mail,description,groupTypes&$top={top}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        groups = data.get("value", [])
        return {
            "status": "success",
            "groups": groups,
            "count": len(groups),
            "query": query,
            "message": json.dumps(groups, indent=2)
        }
    except Exception as error:
        logger.error(f"Error searching groups: {error}")
        return {"status": "error", "message": f"Error searching groups: {str(error)}"}


async def EID_createUserGroups(
    groupName: str,
    description: Optional[str] = None,
    userIds: Optional[List[str]] = None,
    groupIds: Optional[List[str]] = None,
    mailEnabled: bool = False,
    addPrefix: bool = False
) -> dict[str, Any]:
    """
    Create and manage Entra ID security groups with users and nested groups.
    
    This tool creates static membership security groups in Microsoft Entra ID, with support for
    adding both user members and nested groups. Groups can be configured as mail-enabled or
    security-only, making them suitable for various enterprise identity scenarios including
    access control, application assignments, and governance policies.
    
    Args:
        groupName: Name for the group (optionally prefixed based on addPrefix parameter)
        description: Description of the group's purpose and membership
        userIds: Array of user object IDs to add as members
        groupIds: Array of group object IDs to add as nested groups
        mailEnabled: Whether the group is mail-enabled (default: False for security groups)
        addPrefix: Whether to add 'POC-' prefix to group name for testing environments (default: False)
        
    Returns:
        Dictionary with detailed creation results including group ID, member counts, and any errors.
    """
    logger.info(f"EID_createUserGroups called: groupName={groupName}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        results = []
        results.append("╔════════════════════════════════════════════════════════════════╗")
        results.append("║  Entra ID Group Creation                                       ║")
        results.append("╚════════════════════════════════════════════════════════════════╝")
        results.append("")
        
        # Add prefix only if explicitly requested
        if addPrefix and not groupName.startswith("POC-"):
            final_group_name = f"POC-{groupName}"
        else:
            final_group_name = groupName
        
        # Initialize lists if None
        if userIds is None:
            userIds = []
        if groupIds is None:
            groupIds = []
        
        # Validate inputs
        total_members = len(userIds) + len(groupIds)
        if total_members == 0:
            results.append("⚠️  Warning: No members specified. Creating empty group.")
            results.append("   You can add members later via Azure Portal or API.")
            results.append("")
        
        if total_members > 100:
            results.append("⚠️  Warning: Adding more than 100 members may take a while")
            results.append("")
        
        # ========================================================================
        # STEP 1: Create the Group
        # ========================================================================
        results.append("📋 Step 1: Creating Security Group")
        results.append(f"   Group Name: {final_group_name}")
        results.append(f"   Mail Enabled: {mailEnabled}")
        results.append("   Security Enabled: true")
        results.append("")
        
        # Create mail nickname (alphanumeric only, max 64 chars)
        mail_nickname = ''.join(c for c in final_group_name if c.isalnum()).lower()[:64]
        if not mail_nickname:
            mail_nickname = "pocgroup"
        
        group_body = {
            "displayName": final_group_name,
            "description": description or f"Security group - {final_group_name}",
            "mailEnabled": mailEnabled,
            "mailNickname": mail_nickname,
            "securityEnabled": True,
            "groupTypes": []  # Static membership
        }
        
        results.append("🔄 Creating group via Microsoft Graph API...")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            group_response = await client.post(
                "https://graph.microsoft.com/v1.0/groups",
                headers=headers,
                json=group_body
            )
            group_response.raise_for_status()
            group_data = group_response.json()
        
        group_id = group_data["id"]
        
        results.append("✅ Group created successfully!")
        results.append("")
        results.append("📊 Group Details:")
        results.append(f"   Group ID: {group_id}")
        results.append(f"   Display Name: {group_data['displayName']}")
        results.append(f"   Mail Nickname: {group_data['mailNickname']}")
        results.append("")
        
        # ========================================================================
        # STEP 2: Add User Members
        # ========================================================================
        added_users = []
        failed_users = []
        
        if userIds and len(userIds) > 0:
            results.append("📋 Step 2: Adding User Members")
            results.append(f"   Number of users to add: {len(userIds)}")
            results.append("")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                for i, user_id in enumerate(userIds):
                    try:
                        results.append(f"   [{i + 1}/{len(userIds)}] Adding user: {user_id}")
                        
                        member_response = await client.post(
                            f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref",
                            headers=headers,
                            json={"@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"}
                        )
                        member_response.raise_for_status()
                        
                        added_users.append(user_id)
                        
                        # Add small delay to avoid throttling
                        if i < len(userIds) - 1:
                            await asyncio.sleep(0.1)
                    except Exception as error:
                        error_msg = str(error)
                        results.append(f"      ❌ Failed: {error_msg}")
                        failed_users.append({"userId": user_id, "error": error_msg})
            
            results.append("")
            results.append("📊 User Addition Summary:")
            results.append(f"   Successfully added: {len(added_users)}")
            results.append(f"   Failed: {len(failed_users)}")
            
            if failed_users:
                results.append("")
                results.append("⚠️  Failed Users:")
                for item in failed_users:
                    results.append(f"   - {item['userId']}: {item['error']}")
            results.append("")
        
        # ========================================================================
        # STEP 3: Add Group Members (Nested Groups)
        # ========================================================================
        added_groups = []
        failed_groups = []
        
        if groupIds and len(groupIds) > 0:
            step_num = 3 if userIds and len(userIds) > 0 else 2
            results.append(f"📋 Step {step_num}: Adding Nested Groups")
            results.append(f"   Number of groups to add: {len(groupIds)}")
            results.append("")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                for i, nested_group_id in enumerate(groupIds):
                    try:
                        results.append(f"   [{i + 1}/{len(groupIds)}] Adding group: {nested_group_id}")
                        
                        member_response = await client.post(
                            f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref",
                            headers=headers,
                            json={"@odata.id": f"https://graph.microsoft.com/v1.0/groups/{nested_group_id}"}
                        )
                        member_response.raise_for_status()
                        
                        added_groups.append(nested_group_id)
                        
                        # Add small delay to avoid throttling
                        if i < len(groupIds) - 1:
                            await asyncio.sleep(0.1)
                    except Exception as error:
                        error_msg = str(error)
                        results.append(f"      ❌ Failed: {error_msg}")
                        failed_groups.append({"groupId": nested_group_id, "error": error_msg})
            
            results.append("")
            results.append("📊 Group Addition Summary:")
            results.append(f"   Successfully added: {len(added_groups)}")
            results.append(f"   Failed: {len(failed_groups)}")
            
            if failed_groups:
                results.append("")
                results.append("⚠️  Failed Groups:")
                for item in failed_groups:
                    results.append(f"   - {item['groupId']}: {item['error']}")
            results.append("")
        
        # ========================================================================
        # STEP 4: Verify Group Status
        # ========================================================================
        step_num = 1
        if userIds and len(userIds) > 0:
            step_num += 1
        if groupIds and len(groupIds) > 0:
            step_num += 1
        step_num += 1
        
        results.append(f"📋 Step {step_num}: Verifying Group Status")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                verify_response = await client.get(
                    f"https://graph.microsoft.com/v1.0/groups/{group_id}?$select=id,displayName,description,mailEnabled,securityEnabled",
                    headers=headers
                )
                verify_response.raise_for_status()
                
                # Get member count
                try:
                    members_response = await client.get(
                        f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$select=id",
                        headers=headers
                    )
                    members_response.raise_for_status()
                    members_data = members_response.json()
                    results.append(f"   Total members: {len(members_data.get('value', []))}")
                except Exception:
                    results.append("   Total members: Unable to retrieve")
        except Exception as verify_error:
            results.append(f"   ⚠️  Could not verify group status: {str(verify_error)}")
        
        # ========================================================================
        # SUCCESS SUMMARY
        # ========================================================================
        results.append("")
        results.append("╔════════════════════════════════════════════════════════════════╗")
        results.append("║  ✅ GROUP CREATION COMPLETE                                    ║")
        results.append("╚════════════════════════════════════════════════════════════════╝")
        results.append("")
        results.append("📱 Group Information:")
        results.append(f"   Group ID: {group_id}")
        results.append(f"   Display Name: {final_group_name}")
        results.append("   Type: Security Group (Static Membership)")
        results.append(f"   Users Added: {len(added_users)}{f' ({len(failed_users)} failed)' if failed_users else ''}")
        results.append(f"   Groups Added: {len(added_groups)}{f' ({len(failed_groups)} failed)' if failed_groups else ''}")
        results.append("")
        results.append("🔗 Useful Links:")
        results.append(f"   View in Azure Portal: https://portal.azure.com/#view/Microsoft_AAD_IAM/GroupDetailsMenuBlade/~/Overview/groupId/{group_id}")
        results.append(f"   Manage members: https://portal.azure.com/#view/Microsoft_AAD_IAM/GroupDetailsMenuBlade/~/Members/groupId/{group_id}")
        results.append("")
        results.append("📚 Next Steps:")
        results.append("   1. Assign Entra ID roles to this group")
        results.append("   2. Use group in Conditional Access policies")
        results.append("   3. Assign applications to the group")
        results.append("   4. Configure group-based licensing")
        results.append("   5. Set up dynamic membership rules if needed")
        
        # Return JSON response
        response = {
            "success": len(failed_users) == 0 and len(failed_groups) == 0,
            "group": {
                "id": group_id,
                "displayName": final_group_name,
                "description": description or f"Security group - {final_group_name}",
                "securityEnabled": True,
                "mailEnabled": mailEnabled
            },
            "members": {
                "users": {
                    "requested": len(userIds),
                    "added": len(added_users),
                    "failed": len(failed_users)
                },
                "groups": {
                    "requested": len(groupIds),
                    "added": len(added_groups),
                    "failed": len(failed_groups)
                }
            },
            "errors": {
                "users": failed_users if failed_users else None,
                "groups": failed_groups if failed_groups else None
            }
        }
        
        results.append("")
        results.append("📄 JSON Response:")
        results.append(json.dumps(response, indent=2))
        
        return {
            "status": "success",
            "message": '\n'.join(results),
            "data": response
        }
        
    except Exception as error:
        results = []
        results.append("")
        results.append("╔════════════════════════════════════════════════════════════════╗")
        results.append("║  ❌ ERROR OCCURRED                                             ║")
        results.append("╚════════════════════════════════════════════════════════════════╝")
        results.append(f"Error: {str(error)}")
        
        # Return error in JSON format
        results.append("")
        results.append("📄 Error Response:")
        error_response = {
            "success": False,
            "error": str(error)
        }
        results.append(json.dumps(error_response, indent=2))
        
        logger.error(f"Error in EID_createUserGroups: {error}")
        
        return {
            "status": "error",
            "message": '\n'.join(results),
            "data": error_response
        }
