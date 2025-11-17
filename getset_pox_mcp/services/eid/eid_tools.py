"""
EID (Entra ID) MCP tools registration.

This module defines the MCP tool schemas for the Entra ID service.
"""

from mcp.types import Tool

def get_EID_listUsers_tool() -> Tool:
    """Get the MCP Tool definition for EID_listUsers."""
    return Tool(
        name="EID_listUsers",
        description="List all users from Microsoft Entra ID (Azure AD) via Graph API v1.0",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

def get_EID_getUser_tool() -> Tool:
    """Get the MCP Tool definition for EID_getUser."""
    return Tool(
        name="EID_getUser",
        description="Get a specific user by ID or userPrincipalName from Microsoft Entra ID",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID or userPrincipalName of the user",
                },
            },
            "required": ["user_id"],
        },
    )

def get_EID_searchUsers_tool() -> Tool:
    """Get the MCP Tool definition for EID_searchUsers."""
    return Tool(
        name="EID_searchUsers",
        description="Search for users in Microsoft Entra ID by display name or email address",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string to match against displayName or userPrincipalName",
                },
                "top": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 50, max: 999)",
                    "default": 50,
                },
            },
            "required": ["query"],
        },
    )

def get_EID_listDevices_tool() -> Tool:
    """Get the MCP Tool definition for EID_listDevices."""
    return Tool(
        name="EID_listDevices",
        description="List all devices including Entra Joined, Entra Hybrid Joined, Registered, and Compliant Devices from Microsoft Entra ID",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

def get_EID_getDevice_tool() -> Tool:
    """Get the MCP Tool definition for EID_getDevice."""
    return Tool(
        name="EID_getDevice",
        description="Get a specific device by ID from Microsoft Entra ID",
        inputSchema={
            "type": "object",
            "properties": {
                "device_id": {
                    "type": "string",
                    "description": "The ID of the device",
                },
            },
            "required": ["device_id"],
        },
    )

def get_EID_getGroups_tool() -> Tool:
    """Get the MCP Tool definition for EID_getGroups."""
    return Tool(
        name="EID_getGroups",
        description="List all groups from Microsoft Entra ID with basic details",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "type": "integer",
                    "description": "Maximum number of groups to return (default: 100, max: 999)",
                    "default": 100,
                },
            },
            "required": [],
        },
    )

def get_EID_getGroup_tool() -> Tool:
    """Get the MCP Tool definition for EID_getGroup."""
    return Tool(
        name="EID_getGroup",
        description="Get a specific group by ID from Microsoft Entra ID",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "string",
                    "description": "The ID of the group",
                },
            },
            "required": ["group_id"],
        },
    )

def get_EID_getGroupMembers_tool() -> Tool:
    """Get the MCP Tool definition for EID_getGroupMembers."""
    return Tool(
        name="EID_getGroupMembers",
        description="Get members of a specific group from Microsoft Entra ID",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "string",
                    "description": "The ID of the group",
                },
                "top": {
                    "type": "integer",
                    "description": "Maximum number of members to return (default: 100, max: 999)",
                    "default": 100,
                },
            },
            "required": ["group_id"],
        },
    )

def get_EID_searchGroups_tool() -> Tool:
    """Get the MCP Tool definition for EID_searchGroups."""
    return Tool(
        name="EID_searchGroups",
        description="Search for groups in Microsoft Entra ID by display name",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string to match against group displayName",
                },
                "top": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 50, max: 999)",
                    "default": 50,
                },
            },
            "required": ["query"],
        },
    )

def get_EID_createUserGroups_tool() -> Tool:
    """Get the MCP Tool definition for EID_createUserGroups."""
    return Tool(
        name="EID_createUserGroups",
        description="Create and manage Entra ID security groups with users and nested groups. Creates static membership security groups suitable for access control, application assignments, and governance policies.",
        inputSchema={
            "type": "object",
            "properties": {
                "groupName": {
                    "type": "string",
                    "description": "Name for the group (optionally prefixed based on addPrefix parameter)",
                },
                "description": {
                    "type": "string",
                    "description": "Description of the group's purpose and membership",
                },
                "userIds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of user object IDs to add as members",
                    "default": [],
                },
                "groupIds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of group object IDs to add as nested groups",
                    "default": [],
                },
                "mailEnabled": {
                    "type": "boolean",
                    "description": "Whether the group is mail-enabled (default: False for security groups)",
                    "default": False,
                },
                "addPrefix": {
                    "type": "boolean",
                    "description": "Whether to add 'POC-' prefix to group name for testing environments",
                    "default": False,
                },
            },
            "required": ["groupName"],
        },
    )
