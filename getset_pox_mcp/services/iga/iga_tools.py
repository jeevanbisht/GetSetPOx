"""
IGA Tools MCP registration.

This module defines the MCP tool schemas for the IGA service.
"""

from mcp.types import Tool

def get_IGA_listAccessPackages_tool() -> Tool:
    """Get the MCP Tool definition for IGA_listAccessPackages."""
    return Tool(
        name="IGA_listAccessPackages",
        description="Retrieves all access packages from Microsoft Entra ID's Entitlement Management. Access packages are collections of resources (groups, apps, sites) that users can request access to.",
        inputSchema={
            "type": "object",
            "properties": {
                "select": {
                    "type": "string",
                    "description": "OData $select query to return specific properties (e.g., 'id,displayName,description')"
                },
                "filter": {
                    "type": "string",
                    "description": "OData $filter query to narrow results (e.g., \"contains(tolower(displayName),'team')\")"
                },
                "expand": {
                    "type": "string",
                    "description": "OData $expand query to include related entities (e.g., 'accessPackageCatalog')"
                }
            },
            "required": [],
        },
    )

def get_IGA_createAccessCatalog_tool() -> Tool:
    """Get the MCP Tool definition for IGA_createAccessCatalog."""
    return Tool(
        name="IGA_createAccessCatalog",
        description="Creates a new access package catalog in Microsoft Entra ID's Entitlement Management. Catalogs are containers for access packages and their related resources.",
        inputSchema={
            "type": "object",
            "properties": {
                "displayName": {
                    "type": "string",
                    "description": "The display name of the access package catalog"
                },
                "description": {
                    "type": "string",
                    "description": "The description of the access package catalog"
                },
                "state": {
                    "type": "string",
                    "description": "The state of the catalog",
                    "enum": ["published", "unpublished"]
                },
                "isExternallyVisible": {
                    "type": "boolean",
                    "description": "Whether external users can request access packages from this catalog"
                }
            },
            "required": ["displayName", "description", "state", "isExternallyVisible"],
        },
    )

def get_IGA_createAccessPackage_tool() -> Tool:
    """Get the MCP Tool definition for IGA_createAccessPackage."""
    return Tool(
        name="IGA_createAccessPackage",
        description="Creates a new access package in Microsoft Entra ID's Entitlement Management. Access packages define what resources users get access to and for how long.",
        inputSchema={
            "type": "object",
            "properties": {
                "catalogId": {
                    "type": "string",
                    "description": "The ID of the catalog that this access package will be linked to"
                },
                "displayName": {
                    "type": "string",
                    "description": "The display name of the access package"
                },
                "description": {
                    "type": "string",
                    "description": "The description of the access package (optional)"
                }
            },
            "required": ["catalogId", "displayName"],
        },
    )

def get_IGA_addResourceGrouptoPackage_tool() -> Tool:
    """Get the MCP Tool definition for IGA_addResourceGrouptoPackage."""
    return Tool(
        name="IGA_addResourceGrouptoPackage",
        description="Adds a Microsoft Entra group as a resource to an existing access package. Implements a two-step workflow: adds the group to the catalog and links the group resource role to the access package.",
        inputSchema={
            "type": "object",
            "properties": {
                "catalogId": {
                    "type": "string",
                    "description": "The Entra access catalog ID"
                },
                "accessPackageId": {
                    "type": "string",
                    "description": "The ID of the access package"
                },
                "groupObjectId": {
                    "type": "string",
                    "description": "The Azure AD Object ID of the group to add"
                }
            },
            "required": ["catalogId", "accessPackageId", "groupObjectId"],
        },
    )
