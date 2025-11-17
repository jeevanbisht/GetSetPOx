"""
Intune service package.

This package provides tools for Microsoft Intune device management and app deployment.
"""

from getset_pox_mcp.services.intune.intune_service import (
    IN_listIntuneManagedDevices,
    IN_getManagedDeviceDetails,
    IN_listDeviceCompliancePolicies,
    IN_listDeviceConfigurationProfiles,
    IN_syncManagedDevice,
    IN_prepGSAWinClient,
    IN_intuneAppAssignment,
)

__all__ = [
    "IN_listIntuneManagedDevices",
    "IN_getManagedDeviceDetails",
    "IN_listDeviceCompliancePolicies",
    "IN_listDeviceConfigurationProfiles",
    "IN_syncManagedDevice",
    "IN_prepGSAWinClient",
    "IN_intuneAppAssignment",
]
