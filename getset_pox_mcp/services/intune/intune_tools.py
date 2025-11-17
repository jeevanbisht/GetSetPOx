"""
Intune Tools MCP registration.

This module defines the MCP tool schemas for the Intune service.
"""

from mcp.types import Tool

def get_IN_listIntuneManagedDevices_tool() -> Tool:
    """Get the MCP Tool definition for IN_listIntuneManagedDevices."""
    return Tool(
        name="IN_listIntuneManagedDevices",
        description="List all managed devices in Microsoft Intune with their basic information (device name, OS, user, ID).",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "type": "integer",
                    "description": "Number of devices to return (default: 10)",
                    "default": 10
                }
            },
            "required": [],
        },
    )

def get_IN_getManagedDeviceDetails_tool() -> Tool:
    """Get the MCP Tool definition for IN_getManagedDeviceDetails."""
    return Tool(
        name="IN_getManagedDeviceDetails",
        description="Get detailed information about a specific managed device in Microsoft Intune including compliance state, enrollment date, last sync, serial number, model, and manufacturer.",
        inputSchema={
            "type": "object",
            "properties": {
                "deviceId": {
                    "type": "string",
                    "description": "The ID of the managed device"
                }
            },
            "required": ["deviceId"],
        },
    )

def get_IN_listDeviceCompliancePolicies_tool() -> Tool:
    """Get the MCP Tool definition for IN_listDeviceCompliancePolicies."""
    return Tool(
        name="IN_listDeviceCompliancePolicies",
        description="List all device compliance policies in Microsoft Intune showing policy names, platforms, and descriptions.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

def get_IN_listDeviceConfigurationProfiles_tool() -> Tool:
    """Get the MCP Tool definition for IN_listDeviceConfigurationProfiles."""
    return Tool(
        name="IN_listDeviceConfigurationProfiles",
        description="List all device configuration profiles in Microsoft Intune showing profile names, platforms, and descriptions.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

def get_IN_syncManagedDevice_tool() -> Tool:
    """Get the MCP Tool definition for IN_syncManagedDevice."""
    return Tool(
        name="IN_syncManagedDevice",
        description="Trigger a sync for a specific managed device in Microsoft Intune. The device will sync when it next checks in with Intune.",
        inputSchema={
            "type": "object",
            "properties": {
                "deviceId": {
                    "type": "string",
                    "description": "The ID of the managed device to sync"
                }
            },
            "required": ["deviceId"],
        },
    )

def get_IN_prepGSAWinClient_tool() -> Tool:
    """Get the MCP Tool definition for IN_prepGSAWinClient."""
    return Tool(
        name="IN_prepGSAWinClient",
        description="Prepares installation of the Global Secure Access (GSA) Windows Client for Microsoft Intune. Downloads the GSA client and uploads it to Intune (complex multi-step operation - currently informational).",
        inputSchema={
            "type": "object",
            "properties": {
                "displayName": {
                    "type": "string",
                    "description": "Display name for the app in Intune",
                    "default": "Global Secure Access Client"
                },
                "description": {
                    "type": "string",
                    "description": "Description of the GSA Windows Client app",
                    "default": "Microsoft Global Secure Access Windows client for secure network connectivity"
                },
                "publisher": {
                    "type": "string",
                    "description": "Publisher name",
                    "default": "Microsoft"
                },
                "sasUrl": {
                    "type": "string",
                    "description": "Optional custom SAS URL for the installer package"
                }
            },
            "required": [],
        },
    )

def get_IN_intuneAppAssignment_tool() -> Tool:
    """Get the MCP Tool definition for IN_intuneAppAssignment."""
    return Tool(
        name="IN_intuneAppAssignment",
        description="Assign device groups to Intune Win32 applications with configurable deployment settings. Supports required (auto-install), available (user-initiated), or uninstall deployment intents.",
        inputSchema={
            "type": "object",
            "properties": {
                "appId": {
                    "type": "string",
                    "description": "The Win32 LOB App ID to assign groups to"
                },
                "groupIds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of Entra ID group object IDs to assign the app to"
                },
                "intent": {
                    "type": "string",
                    "description": "Deployment intent",
                    "enum": ["required", "available", "uninstall"],
                    "default": "required"
                },
                "notificationSettings": {
                    "type": "string",
                    "description": "Notification display level",
                    "enum": ["showAll", "showReboot", "hideAll"],
                    "default": "showAll"
                },
                "restartGracePeriod": {
                    "type": "integer",
                    "description": "Grace period in minutes before forcing restart (default: 1440 = 24 hours)",
                    "default": 1440
                },
                "deliveryOptimizationPriority": {
                    "type": "string",
                    "description": "Delivery optimization priority",
                    "enum": ["notConfigured", "foreground"],
                    "default": "notConfigured"
                }
            },
            "required": ["appId", "groupIds"],
        },
    )
