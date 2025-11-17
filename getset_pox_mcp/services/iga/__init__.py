"""
IGA (Identity Governance and Administration) service package.

This package provides tools for Microsoft Entra ID Entitlement Management.
"""

from getset_pox_mcp.services.iga.iga_service import (
    IGA_listAccessPackages,
    IGA_createAccessCatalog,
    IGA_createAccessPackage,
    IGA_addResourceGrouptoPackage,
)

__all__ = [
    "IGA_listAccessPackages",
    "IGA_createAccessCatalog",
    "IGA_createAccessPackage",
    "IGA_addResourceGrouptoPackage",
]
