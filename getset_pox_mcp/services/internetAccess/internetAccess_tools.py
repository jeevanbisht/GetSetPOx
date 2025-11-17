"""
Internet Access MCP tools registration.

This module defines the MCP tool schemas for the Internet Access service.
"""

from mcp.types import Tool

def get_IA_checkInternetAccessForwardingProfile_tool() -> Tool:
    """Get the MCP Tool definition for IA_checkInternetAccessForwardingProfile."""
    return Tool(
        name="IA_checkInternetAccessForwardingProfile",
        description="Check if the Internet Access Forwarding Profile is enabled in Entra Global Secure Access",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

def get_IA_enableInternetAccessForwardingProfile_tool() -> Tool:
    """Get the MCP Tool definition for IA_enableInternetAccessForwardingProfile."""
    return Tool(
        name="IA_enableInternetAccessForwardingProfile",
        description="Enable or disable the Internet Access Forwarding Profile in Entra Global Secure Access",
        inputSchema={
            "type": "object",
            "properties": {
                "forwarding_profile_id": {
                    "type": "string",
                    "description": "ID of the forwarding profile to enable/disable",
                },
                "state": {
                    "type": "string",
                    "description": "Target state (enabled or disabled)",
                    "default": "enabled",
                    "enum": ["enabled", "disabled"],
                },
            },
            "required": ["forwarding_profile_id"],
        },
    )

def get_IA_createFilteringPolicy_tool() -> Tool:
    """Get the MCP Tool definition for IA_createFilteringPolicy."""
    return Tool(
        name="IA_createFilteringPolicy",
        description="Create a web category filtering policy for Entra Global Secure Access",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the filtering policy",
                    "default": "POC-Monitor AI Access",
                },
                "description": {
                    "type": "string",
                    "description": "Description of the filtering policy",
                    "default": "Monitor access to AI",
                },
                "webCategories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of web category names to filter (e.g., ArtificialIntelligence, Gambling)",
                    "default": ["ArtificialIntelligence"],
                },
            },
            "required": [],
        },
    )

def get_IA_createFilteringProfile_tool() -> Tool:
    """Get the MCP Tool definition for IA_createFilteringProfile."""
    return Tool(
        name="IA_createFilteringProfile",
        description="Create a filtering profile in Entra Global Secure Access",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the filtering profile",
                    "default": "POC-Monitor AI Access Profile",
                },
                "description": {
                    "type": "string",
                    "description": "Description of the filtering profile",
                    "default": "Profile for monitoring AI access",
                },
                "state": {
                    "type": "string",
                    "description": "Initial state of the profile",
                    "default": "enabled",
                    "enum": ["enabled", "disabled"],
                },
                "priority": {
                    "type": "integer",
                    "description": "Priority of the profile",
                    "default": 1000,
                },
            },
            "required": [],
        },
    )

def get_IA_linkPolicyToFilteringProfile_tool() -> Tool:
    """Get the MCP Tool definition for IA_linkPolicyToFilteringProfile."""
    return Tool(
        name="IA_linkPolicyToFilteringProfile",
        description="Link a filtering policy to a filtering profile with logging enabled",
        inputSchema={
            "type": "object",
            "properties": {
                "filtering_profile_id": {
                    "type": "string",
                    "description": "ID of the filtering profile",
                },
                "filtering_policy_id": {
                    "type": "string",
                    "description": "ID of the filtering policy to link",
                },
                "priority": {
                    "type": "integer",
                    "description": "Priority of the link",
                    "default": 1000,
                },
            },
            "required": ["filtering_profile_id", "filtering_policy_id"],
        },
    )

def get_IA_createConditionalAccessPolicy_tool() -> Tool:
    """Get the MCP Tool definition for IA_createConditionalAccessPolicy."""
    return Tool(
        name="IA_createConditionalAccessPolicy",
        description="Create a conditional access policy that references a filtering profile",
        inputSchema={
            "type": "object",
            "properties": {
                "filtering_profile_id": {
                    "type": "string",
                    "description": "ID of the filtering profile to reference",
                },
                "displayName": {
                    "type": "string",
                    "description": "Display name for the conditional access policy",
                    "default": "POC-Monitor AI conditional access policy",
                },
                "includeUsers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of user IDs to include (use 'None' for no specific users)",
                    "default": ["None"],
                },
                "includeGroups": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of group IDs to include",
                    "default": [],
                },
                "includeApplications": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of application IDs to include",
                    "default": [
                        "c08f52c9-8f03-4558-a0ea-9a4c878cf343",
                        "5dc48733-b5df-475c-a49b-fa307ef00853"
                    ],
                },
            },
            "required": ["filtering_profile_id"],
        },
    )

def get_IA_TLSPOCV2_tool() -> Tool:
    """Get the MCP Tool definition for IA_TLSPOCV2."""
    return Tool(
        name="IA_TLSPOCV2",
        description="TLS Onboarding POC V2 - Advanced automated certificate workflow with retry logic for Global Secure Access TLS inspection. Note: This is a placeholder - full implementation requires cryptography library integration.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Certificate name (max 12 characters, alphanumeric only)",
                    "default": "POCEntCA",
                },
                "commonName": {
                    "type": "string",
                    "description": "Common name (max 12 characters, alphanumeric + spaces)",
                    "default": "POCRoot",
                },
                "organizationName": {
                    "type": "string",
                    "description": "Organization name (max 12 characters, alphanumeric only)",
                    "default": "POCLtd",
                },
                "cert_output_dir": {
                    "type": "string",
                    "description": "Directory for certificate storage",
                    "default": "./certs",
                },
                "max_retries": {
                    "type": "integer",
                    "description": "Maximum retry attempts for transient failures",
                    "default": 5,
                },
            },
            "required": [],
        },
    )

def get_IA_internetAccessPoc_tool() -> Tool:
    """Get the MCP Tool definition for IA_internetAccessPoc."""
    return Tool(
        name="IA_internetAccessPoc",
        description="Automated end-to-end setup for Web Content Filtering POC in Entra Global Secure Access. Enables forwarding profile, creates filtering policy and profile, links them, and optionally creates conditional access policy.",
        inputSchema={
            "type": "object",
            "properties": {
                "forwarding_profile_id": {
                    "type": "string",
                    "description": "ID of the forwarding profile to enable",
                },
                "filtering_policy_name": {
                    "type": "string",
                    "description": "Name for the filtering policy",
                    "default": "POC-Monitor AI Access",
                },
                "filtering_policy_description": {
                    "type": "string",
                    "description": "Description for the filtering policy",
                    "default": "Monitor access to AI",
                },
                "filtering_profile_name": {
                    "type": "string",
                    "description": "Name for the filtering profile",
                    "default": "POC-Monitor AI Access Profile",
                },
                "filtering_profile_description": {
                    "type": "string",
                    "description": "Description for the filtering profile",
                    "default": "Profile for monitoring AI access",
                },
                "filtering_profile_state": {
                    "type": "string",
                    "description": "State of the filtering profile",
                    "default": "enabled",
                    "enum": ["enabled", "disabled"],
                },
                "filtering_profile_priority": {
                    "type": "integer",
                    "description": "Priority of the filtering profile",
                    "default": 1000,
                },
                "link_priority": {
                    "type": "integer",
                    "description": "Priority for the policy-to-profile link",
                    "default": 1000,
                },
                "create_ca_policy": {
                    "type": "boolean",
                    "description": "Whether to create a conditional access policy",
                    "default": True,
                },
                "ca_policy_display_name": {
                    "type": "string",
                    "description": "Display name for the conditional access policy",
                    "default": "POC-Monitor AI conditional access policy",
                },
                "ca_policy_include_users": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Users to include in CA policy",
                    "default": ["None"],
                },
                "ca_policy_include_groups": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Groups to include in CA policy",
                    "default": [],
                },
                "ca_policy_include_applications": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Applications to include in CA policy",
                    "default": [
                        "c08f52c9-8f03-4558-a0ea-9a4c878cf343",
                        "5dc48733-b5df-475c-a49b-fa307ef00853"
                    ],
                },
            },
            "required": ["forwarding_profile_id"],
        },
    )
