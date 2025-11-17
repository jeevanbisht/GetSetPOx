"""
Services package for getset-pox-mcp.

This package contains all MCP tool implementations and service modules.
Each service module should define tools that can be registered with the MCP server.
"""

from getset_pox_mcp.services.Test.hello_world_service import hello_world
from getset_pox_mcp.services.Test.echo_service import echo
from getset_pox_mcp.services.diagnostics.diagnostics_service import check_token_permissions
from getset_pox_mcp.services.internetAccess.internetAccess_service import (
    IA_checkInternetAccessForwardingProfile,
    IA_enableInternetAccessForwardingProfile,
    IA_createFilteringPolicy,
    IA_createFilteringProfile,
    IA_linkPolicyToFilteringProfile,
    IA_createConditionalAccessPolicy,
    IA_TLSPOCV2,
    IA_internetAccessPoc,
)
from getset_pox_mcp.services.poc.poc_service import GovernInternetAccessPOC
from getset_pox_mcp.services.iga.iga_service import (
    IGA_listAccessPackages,
    IGA_createAccessCatalog,
    IGA_createAccessPackage,
    IGA_addResourceGrouptoPackage,
)
from getset_pox_mcp.services.intune.intune_service import (
    IN_listIntuneManagedDevices,
    IN_getManagedDeviceDetails,
    IN_listDeviceCompliancePolicies,
    IN_listDeviceConfigurationProfiles,
    IN_syncManagedDevice,
    IN_prepGSAWinClient,
    IN_intuneAppAssignment,
)
from getset_pox_mcp.services.eid.eid_service import (
    EID_listUsers,
    EID_getUser,
    EID_searchUsers,
    EID_listDevices,
    EID_getDevice,
    EID_getGroups,
    EID_getGroup,
    EID_getGroupMembers,
    EID_searchGroups,
    EID_createUserGroups,
)

__all__ = [
    "hello_world",
    "echo",
    "check_token_permissions",
    "IA_checkInternetAccessForwardingProfile",
    "IA_enableInternetAccessForwardingProfile",
    "IA_createFilteringPolicy",
    "IA_createFilteringProfile",
    "IA_linkPolicyToFilteringProfile",
    "IA_createConditionalAccessPolicy",
    "IA_TLSPOCV2",
    "IA_internetAccessPoc",
    "GovernInternetAccessPOC",
    "IGA_listAccessPackages",
    "IGA_createAccessCatalog",
    "IGA_createAccessPackage",
    "IGA_addResourceGrouptoPackage",
    "IN_listIntuneManagedDevices",
    "IN_getManagedDeviceDetails",
    "IN_listDeviceCompliancePolicies",
    "IN_listDeviceConfigurationProfiles",
    "IN_syncManagedDevice",
    "IN_prepGSAWinClient",
    "IN_intuneAppAssignment",
    "EID_listUsers",
    "EID_getUser",
    "EID_searchUsers",
    "EID_listDevices",
    "EID_getDevice",
    "EID_getGroups",
    "EID_getGroup",
    "EID_getGroupMembers",
    "EID_searchGroups",
    "EID_createUserGroups",
]
