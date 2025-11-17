"""
Identity Governance and Administration (IGA) Service Implementation.

This service provides IGA tools for Microsoft Entra ID Entitlement Management
via Microsoft Graph API.

Dependencies:
- httpx: For async HTTP requests
- getset_pox_mcp.authentication.middleware: For authentication token management
"""

from typing import Any, Optional
from getset_pox_mcp.logging_config import get_logger
from getset_pox_mcp.authentication.middleware import get_auth_middleware
import httpx
import json
from datetime import datetime, timezone
import uuid
import time

logger = get_logger(__name__)


async def IGA_listAccessPackages(
    select: Optional[str] = None,
    filter: Optional[str] = None,
    expand: Optional[str] = None
) -> dict[str, Any]:
    """
    Retrieves all access packages from Microsoft Entra ID's Entitlement Management.
    
    Access packages are collections of resources (groups, apps, sites) that users can request access to.
    
    Args:
        select: OData $select query to return specific properties (e.g., "id,displayName,description")
        filter: OData $filter query to narrow results (e.g., "contains(tolower(displayName),'team')")
        expand: OData $expand query to include related entities (e.g., "accessPackageCatalog")
        
    Returns:
        Dictionary containing collection of accessPackage objects or error message.
    """
    logger.info("IGA_listAccessPackages called")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        # Build query URL
        base_url = "https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/accessPackages"
        query_params = []
        
        if select:
            query_params.append(f"$select={select}")
        if filter:
            query_params.append(f"$filter={filter}")
        if expand:
            query_params.append(f"$expand={expand}")
        
        url = base_url if not query_params else f"{base_url}?{'&'.join(query_params)}"
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=60.0)
            response.raise_for_status()
            data = response.json()
        
        access_packages = data.get("value", [])
        
        return {
            "status": "success",
            "accessPackages": access_packages,
            "count": len(access_packages),
            "nextLink": data.get("@odata.nextLink"),
            "message": json.dumps(access_packages, indent=2)
        }
        
    except Exception as error:
        logger.error(f"Error listing access packages: {error}")
        return {"status": "error", "message": f"Error listing access packages: {str(error)}"}


async def IGA_createAccessCatalog(
    displayName: str,
    description: str,
    state: str,
    isExternallyVisible: bool
) -> dict[str, Any]:
    """
    Creates a new access package catalog in Microsoft Entra ID's Entitlement Management.
    
    Catalogs are containers for access packages and their related resources.
    
    Args:
        displayName: The display name of the access package catalog (required)
        description: The description of the access package catalog (required)
        state: The state of the catalog - "published" or "unpublished" (required)
        isExternallyVisible: Whether external users can request access packages from this catalog (required)
        
    Returns:
        Dictionary containing the created accessPackageCatalog object or error message.
    """
    logger.info(f"IGA_createAccessCatalog called: {displayName}")
    
    # Input validation
    if not displayName or not isinstance(displayName, str):
        return {"status": "error", "message": "displayName is required and must be a non-empty string"}
    
    if not description or not isinstance(description, str):
        return {"status": "error", "message": "description is required and must be a non-empty string"}
    
    if state not in ["published", "unpublished"]:
        return {"status": "error", "message": "state must be either 'published' or 'unpublished'"}
    
    if not isinstance(isExternallyVisible, bool):
        return {"status": "error", "message": "isExternallyVisible must be a boolean value"}
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        url = "https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/catalogs"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        request_body = {
            "displayName": displayName,
            "description": description,
            "state": state,
            "isExternallyVisible": isExternallyVisible
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=request_body, timeout=60.0)
            
            if response.status_code == 201:
                catalog_data = response.json()
                logger.info(f"Successfully created access catalog with ID: {catalog_data.get('id')}")
                
                return {
                    "status": "success",
                    "catalog": catalog_data,
                    "message": f"Access catalog '{displayName}' created successfully",
                    "catalogId": catalog_data.get("id"),
                    "details": json.dumps(catalog_data, indent=2)
                }
            else:
                error_data = response.json() if response.text else {}
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                
                return {
                    "status": "error",
                    "message": f"Failed to create catalog: {error_message}",
                    "statusCode": response.status_code
                }
        
    except Exception as error:
        logger.error(f"Error creating access catalog: {error}")
        return {"status": "error", "message": f"Error creating access catalog: {str(error)}"}


async def IGA_createAccessPackage(
    catalogId: str,
    displayName: str,
    description: Optional[str] = None
) -> dict[str, Any]:
    """
    Creates a new access package in Microsoft Entra ID's Entitlement Management.
    
    Access packages define what resources users get access to and for how long.
    
    Args:
        catalogId: The ID of the catalog that this access package will be linked to (required)
        displayName: The display name of the access package (required)
        description: The description of the access package (optional)
        
    Returns:
        Dictionary containing the created accessPackage object or error message.
    """
    logger.info(f"IGA_createAccessPackage called: {displayName}")
    
    # Input validation
    if not catalogId or not isinstance(catalogId, str):
        return {"status": "error", "message": "catalogId is required and must be a non-empty string"}
    
    if not displayName or not isinstance(displayName, str):
        return {"status": "error", "message": "displayName is required and must be a non-empty string"}
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        url = "https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/accessPackages"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        request_body = {
            "catalog": {"id": catalogId},
            "displayName": displayName
        }
        
        if description is not None:
            request_body["description"] = description
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=request_body, timeout=60.0)
            
            if response.status_code == 201:
                package_data = response.json()
                logger.info(f"Successfully created access package with ID: {package_data.get('id')}")
                
                return {
                    "status": "success",
                    "accessPackage": package_data,
                    "message": f"Access package '{displayName}' created successfully",
                    "accessPackageId": package_data.get("id"),
                    "catalogId": catalogId,
                    "details": json.dumps(package_data, indent=2)
                }
            else:
                error_data = response.json() if response.text else {}
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                
                return {
                    "status": "error",
                    "message": f"Failed to create access package: {error_message}",
                    "statusCode": response.status_code
                }
        
    except Exception as error:
        logger.error(f"Error creating access package: {error}")
        return {"status": "error", "message": f"Error creating access package: {str(error)}"}


async def IGA_addResourceGrouptoPackage(
    catalogId: str,
    accessPackageId: str,
    groupObjectId: str
) -> dict[str, Any]:
    """
    Adds a Microsoft Entra group as a resource to an existing access package.
    
    Implements a two-step workflow:
    1. Add the group to the catalog as a resource
    2. Link the group resource role (Member) to the access package
    
    Args:
        catalogId: The Entra access catalog ID (required)
        accessPackageId: The ID of the access package (required) 
        groupObjectId: The Azure AD Object ID of the group to add (required)
        
    Returns:
        Dictionary containing operation result with confirmation of successful group addition.
    """
    logger.info(f"IGA_addResourceGrouptoPackage called: group={groupObjectId}")
    
    # Input validation
    if not catalogId or not isinstance(catalogId, str):
        return {"status": "error", "message": "catalogId is required and must be a non-empty string"}
    
    if not accessPackageId or not isinstance(accessPackageId, str):
        return {"status": "error", "message": "accessPackageId is required and must be a non-empty string"}
    
    if not groupObjectId or not isinstance(groupObjectId, str):
        return {"status": "error", "message": "groupObjectId is required and must be a non-empty string"}
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        correlation_id = str(uuid.uuid4())
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "x-correlation-id": correlation_id
        }
        
        logger.info(f"Starting group resource addition - Correlation ID: {correlation_id}")
        
        async with httpx.AsyncClient() as client:
            # Step 1: Add the Group to the Catalog
            logger.info(f"Step 1: Adding group {groupObjectId} to catalog {catalogId}")
            
            resource_request_url = "https://graph.microsoft.com/beta/identityGovernance/entitlementManagement/accessPackageResourceRequests"
            resource_request_payload = {
                "catalogId": catalogId,
                "requestType": "AdminAdd",
                "justification": f"Adding group resource via IGA Tool - Correlation ID: {correlation_id}",
                "accessPackageResource": {
                    "resourceType": "AadGroup",
                    "originId": groupObjectId,
                    "originSystem": "AadGroup"
                }
            }
            
            response = await client.post(resource_request_url, headers=headers, json=resource_request_payload, timeout=60.0)
            
            if response.status_code == 201:
                logger.info(f"✅ Step 1 completed: Group added to catalog successfully")
            elif response.status_code == 409:
                logger.info(f"ℹ️ Step 1: Group already exists in catalog, proceeding to step 2")
            else:
                error_data = response.json() if response.text else {}
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                
                return {
                    "status": "error",
                    "step": "add_to_catalog",
                    "message": f"Failed to add group to catalog: {error_message}",
                    "statusCode": response.status_code,
                    "correlationId": correlation_id
                }
            
            # Wait for resource processing
            await asyncio.sleep(3)
            
            # Step 2: Get the resource ID from catalog
            logger.info(f"Step 2: Retrieving resource ID for group {groupObjectId}")
            
            catalog_resources_url = f"https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/catalogs/{catalogId}/accessPackageResources?$filter=originId eq '{groupObjectId}'"
            
            resources_response = await client.get(catalog_resources_url, headers=headers, timeout=60.0)
            
            if resources_response.status_code != 200:
                error_data = resources_response.json() if resources_response.text else {}
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                
                return {
                    "status": "error",
                    "step": "get_resource_id",
                    "message": f"Failed to retrieve resource from catalog: {error_message}",
                    "statusCode": resources_response.status_code,
                    "correlationId": correlation_id
                }
            
            resources_data = resources_response.json()
            resources = resources_data.get("value", [])
            
            if not resources:
                return {
                    "status": "error",
                    "step": "get_resource_id",
                    "message": f"Group resource {groupObjectId} not found in catalog {catalogId}",
                    "correlationId": correlation_id
                }
            
            resource_id = resources[0]["id"]
            logger.info(f"✅ Step 2 completed: Found resource ID: {resource_id}")
            
            # Step 3: Link the Group Resource Role to the Access Package
            logger.info(f"Step 3: Linking group resource role to access package {accessPackageId}")
            
            role_scope_url = f"https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/accessPackages/{accessPackageId}/accessPackageResourceRoleScopes"
            role_scope_payload = {
                "role": {
                    "originId": f"Member_{groupObjectId}",
                    "displayName": "Member",
                    "originSystem": "AadGroup",
                    "resource": {
                        "id": resource_id,
                        "resourceType": "Security Group",
                        "originId": groupObjectId,
                        "originSystem": "AadGroup"
                    }
                },
                "scope": {
                    "originId": groupObjectId,
                    "originSystem": "AadGroup"
                }
            }
            
            role_response = await client.post(role_scope_url, headers=headers, json=role_scope_payload, timeout=60.0)
            
            if role_response.status_code == 201:
                role_scope_data = role_response.json()
                logger.info(f"✅ Step 3 completed: Group role linked successfully")
                
                return {
                    "status": "success",
                    "message": "✅ Group resource has been successfully added to access package",
                    "data": {
                        "catalogId": catalogId,
                        "accessPackageId": accessPackageId,
                        "groupObjectId": groupObjectId,
                        "resourceId": resource_id,
                        "roleId": role_scope_data.get("id"),
                        "role": "Member"
                    },
                    "correlationId": correlation_id
                }
            elif role_response.status_code == 409:
                logger.info(f"ℹ️ Step 3: Group role already assigned")
                
                return {
                    "status": "success",
                    "message": "✅ Group resource is already assigned to access package",
                    "data": {
                        "catalogId": catalogId,
                        "accessPackageId": accessPackageId,
                        "groupObjectId": groupObjectId,
                        "resourceId": resource_id,
                        "role": "Member"
                    },
                    "correlationId": correlation_id
                }
            else:
                error_data = role_response.json() if response.text else {}
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                
                return {
                    "status": "error",
                    "step": "link_role_to_package",
                    "message": f"Failed to link group role: {error_message}",
                    "statusCode": role_response.status_code,
                    "correlationId": correlation_id
                }
        
    except Exception as error:
        logger.error(f"Error adding group resource: {error}")
        return {"status": "error", "message": f"Error adding group resource: {str(error)}"}


# Import asyncio for sleep
import asyncio
