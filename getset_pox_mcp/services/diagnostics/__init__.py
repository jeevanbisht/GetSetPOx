"""
Diagnostics service package.

This package contains diagnostic tools for troubleshooting Microsoft Graph API 
permissions and connectivity, adapted from the EntraSuiteProd project.
"""

from getset_pox_mcp.services.diagnostics.diagnostics_service import check_token_permissions

__all__ = ["check_token_permissions"]
