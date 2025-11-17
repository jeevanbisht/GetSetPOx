"""
Internet Access Service Module
Provides Entra Global Secure Access (Internet Access) management tools
"""

from .internetAccess_service import (
    IA_checkInternetAccessForwardingProfile,
    IA_enableInternetAccessForwardingProfile,
    IA_createFilteringPolicy,
    IA_createFilteringProfile,
    IA_linkPolicyToFilteringProfile,
    IA_createConditionalAccessPolicy,
    IA_internetAccessPoc,
)

__all__ = [
    "IA_checkInternetAccessForwardingProfile",
    "IA_enableInternetAccessForwardingProfile",
    "IA_createFilteringPolicy",
    "IA_createFilteringProfile",
    "IA_linkPolicyToFilteringProfile",
    "IA_createConditionalAccessPolicy",
    "IA_internetAccessPoc",
]
