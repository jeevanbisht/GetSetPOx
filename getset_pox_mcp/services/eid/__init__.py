"""
EID (Entra ID) service package.

This package provides Microsoft Entra ID user and device management tools.
"""

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
