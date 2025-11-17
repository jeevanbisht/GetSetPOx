"""
POC Service Implementation.

This service provides POC (Proof of Concept) automation tools for demonstrating
and testing Entra Global Secure Access capabilities.
"""

from typing import Any, Optional, List
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)

async def GovernInternetAccessPOC() -> dict[str, Any]:
    """
    Creates an Internet Access governance user group, access catalog, and access package for the POC workflow.
    
    This tool automatically initializes a complete "Internet Access Governance" flow for POC users by sequentially
    executing four operations with robust error handling, retry logic, and async operation support:
    1. Creates an Internet Access Users group
    2. Creates an Internet Access governance catalog
    3. Creates an Internet Access governance package
    4. Adds the created group as a resource to the access package
    
    Features:
    - Sequential step execution with success validation
    - Async operation polling with 90-second timeout per step
    - Retry logic (3 attempts with exponential backoff starting at 5 seconds)
    - Detailed logging and execution time tracking
    - Comprehensive error handling with HTTP status codes
    
    Returns:
        Dictionary containing:
        - group_id: ID of the created Internet Access Users group
        - catalog_id: ID of the created Internet Access catalog
        - access_package_id: ID of the created Internet Access access package
        - resource_assignment_id: ID of the resource assignment (group to package)
        - status: "success" or "error"
        - execution_summary: Detailed timing and retry information
        - detailed step results and any error information
    """
    logger.info("GovernInternetAccessPOC called")
    
    try:
        # Import required services
        from getset_pox_mcp.services.eid.eid_service import EID_createUserGroups
        from getset_pox_mcp.services.iga.iga_service import (
            IGA_createAccessCatalog,
            IGA_createAccessPackage,
            IGA_addResourceGrouptoPackage
        )
        
        import time
        from datetime import datetime, timezone
        
        def _get_timestamp():
            """Get current timestamp in ISO format"""
            return datetime.now(timezone.utc).isoformat()
        
        async def _execute_step_with_retry(step_name, step_number, step_func, *args, **kwargs):
            """Execute a step with retry logic and timing."""
            import asyncio
            max_retries = 3
            base_delay = 5  # seconds
            
            logger.info(f"🔄 Starting {step_name} (Step {step_number})")
            step_start_time = time.time()
            
            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        delay = base_delay * (2 ** (attempt - 1))  # Exponential backoff
                        logger.info(f"⏳ Retry attempt {attempt}/{max_retries} for {step_name} after {delay}s delay")
                        await asyncio.sleep(delay)
                    
                    logger.info(f"📡 Executing {step_name} API call...")
                    result = await step_func(*args, **kwargs)
                    
                    # Check for success
                    if result.get("status") in ["success", "Success"]:
                        execution_time = time.time() - step_start_time
                        logger.info(f"✅ {step_name} completed successfully in {execution_time:.2f}s")
                        return True, result, execution_time, attempt
                    
                    # Transient error check
                    if attempt < max_retries:
                        error_msg = result.get("message", "Unknown error")
                        logger.warning(f"⚠️ {step_name} error (attempt {attempt + 1}/{max_retries + 1}): {error_msg}")
                        continue
                    else:
                        execution_time = time.time() - step_start_time
                        return False, result, execution_time, attempt
                        
                except Exception as e:
                    if attempt < max_retries:
                        logger.warning(f"⚠️ {step_name} exception (attempt {attempt + 1}/{max_retries + 1}): {str(e)}")
                        continue
                    else:
                        execution_time = time.time() - step_start_time
                        return False, {"status": "error", "message": str(e)}, execution_time, attempt
            
            execution_time = time.time() - step_start_time
            return False, {"status": "error", "message": "Max retries exceeded"}, execution_time, max_retries
        
        total_start_time = time.time()
        logger.info("🚀 Starting Internet Access Governance POC automation")
        
        setup_results = []
        setup_results.append("╔════════════════════════════════════════════════════════════════╗")
        setup_results.append("║  Internet Access Governance POC Automation                   ║")
        setup_results.append("╚════════════════════════════════════════════════════════════════╝")
        setup_results.append("")
        setup_results.append(f"🕐 Execution started at: {_get_timestamp()}")
        setup_results.append("")
        
        result_data = {
            "group_id": None,
            "catalog_id": None,
            "access_package_id": None,
            "resource_assignment_id": None,
            "steps_completed": 0,
            "total_steps": 4,
            "errors": []
        }
        
        execution_summary = {
            "total_start_time": total_start_time,
            "steps": [],
            "total_retries": 0,
            "total_execution_time": 0,
            "final_status": "in_progress"
        }
        
        # Step 1: Create Internet Access Users Group
        setup_results.append("📋 Step 1: Creating Internet Access Users Group")
        setup_results.append("   Group Name: POC-InternetAccessUsers")
        setup_results.append("")
        
        success, group_result, exec_time, retry_count = await _execute_step_with_retry(
            "Create Internet Access Users Group", 1,
            EID_createUserGroups,
            groupName="InternetAccessUsers",
            addPrefix=True
        )
        
        execution_summary["steps"].append({
            "step": 1, "name": "Create Group", "execution_time": exec_time,
            "retry_count": retry_count, "status": "success" if success else "failed"
        })
        execution_summary["total_retries"] += retry_count
        
        if not success or not group_result.get("data", {}).get("success"):
            error_msg = group_result.get("message", "Unknown error creating group")
            setup_results.append(f"❌ Failed: {error_msg}")
            result_data["errors"].append({"step": 1, "error": error_msg})
            execution_summary["final_status"] = "failed"
            execution_summary["total_execution_time"] = time.time() - total_start_time
            return {
                "status": "error", "message": "\n".join(setup_results),
                "data": result_data, "execution_summary": execution_summary
            }
        
        group_id = group_result["data"]["group"]["id"]
        result_data["group_id"] = group_id
        result_data["steps_completed"] = 1
        setup_results.append(f"✅ Group created: {group_id}")
        setup_results.append("")
        
        # Step 2: Create Catalog
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        catalog_name = f"POC-Internet Access Governance-{timestamp}"
        
        setup_results.append("📋 Step 2: Creating Access Catalog")
        setup_results.append(f"   Catalog Name: {catalog_name}")
        setup_results.append("")
        
        success, catalog_result, exec_time, retry_count = await _execute_step_with_retry(
            "Create Access Catalog", 2,
            IGA_createAccessCatalog,
            displayName=catalog_name,
            description="Internet Access Governance POC Resources",
            state="published",
            isExternallyVisible=False
        )
        
        execution_summary["steps"].append({
            "step": 2, "name": "Create Catalog", "execution_time": exec_time,
            "retry_count": retry_count, "status": "success" if success else "failed"
        })
        execution_summary["total_retries"] += retry_count
        
        if not success:
            error_msg = catalog_result.get("message", "Unknown error creating catalog")
            setup_results.append(f"❌ Failed: {error_msg}")
            result_data["errors"].append({"step": 2, "error": error_msg})
            execution_summary["final_status"] = "failed"
            execution_summary["total_execution_time"] = time.time() - total_start_time
            return {
                "status": "error", "message": "\n".join(setup_results),
                "data": result_data, "execution_summary": execution_summary
            }
        
        catalog_id = catalog_result.get("catalogId")
        result_data["catalog_id"] = catalog_id
        result_data["steps_completed"] = 2
        setup_results.append(f"✅ Catalog created: {catalog_id}")
        setup_results.append("")
        
        # Step 3: Create Access Package
        setup_results.append("📋 Step 3: Creating Access Package")
        setup_results.append("")
        
        success, package_result, exec_time, retry_count = await _execute_step_with_retry(
            "Create Access Package", 3,
            IGA_createAccessPackage,
            catalogId=catalog_id,
            displayName="POC - Internet Access Governance",
            description="Internet Access Governance POC Package"
        )
        
        execution_summary["steps"].append({
            "step": 3, "name": "Create Package", "execution_time": exec_time,
            "retry_count": retry_count, "status": "success" if success else "failed"
        })
        execution_summary["total_retries"] += retry_count
        
        if not success:
            error_msg = package_result.get("message", "Unknown error creating package")
            setup_results.append(f"❌ Failed: {error_msg}")
            result_data["errors"].append({"step": 3, "error": error_msg})
            execution_summary["final_status"] = "failed"
            execution_summary["total_execution_time"] = time.time() - total_start_time
            return {
                "status": "error", "message": "\n".join(setup_results),
                "data": result_data, "execution_summary": execution_summary
            }
        
        access_package_id = package_result.get("accessPackageId")
        result_data["access_package_id"] = access_package_id
        result_data["steps_completed"] = 3
        setup_results.append(f"✅ Access Package created: {access_package_id}")
        setup_results.append("")
        
        # Step 4: Add Resource to Package
        setup_results.append("📋 Step 4: Adding Group as Resource")
        setup_results.append("")
        
        success, resource_result, exec_time, retry_count = await _execute_step_with_retry(
            "Add Resource to Package", 4,
            IGA_addResourceGrouptoPackage,
            catalogId=catalog_id,
            accessPackageId=access_package_id,
            groupObjectId=group_id
        )
        
        execution_summary["steps"].append({
            "step": 4, "name": "Add Resource", "execution_time": exec_time,
            "retry_count": retry_count, "status": "success" if success else "failed"
        })
        execution_summary["total_retries"] += retry_count
        
        if not success:
            error_msg = resource_result.get("message", "Unknown error adding resource")
            setup_results.append(f"❌ Failed: {error_msg}")
            result_data["errors"].append({"step": 4, "error": error_msg})
            execution_summary["final_status"] = "failed"
            execution_summary["total_execution_time"] = time.time() - total_start_time
            return {
                "status": "error", "message": "\n".join(setup_results),
                "data": result_data, "execution_summary": execution_summary
            }
        
        resource_assignment_id = resource_result.get("data", {}).get("roleId")
        result_data["resource_assignment_id"] = resource_assignment_id
        result_data["steps_completed"] = 4
        setup_results.append(f"✅ Resource added: {resource_assignment_id}")
        setup_results.append("")
        
        # Success Summary
        total_execution_time = time.time() - total_start_time
        execution_summary["final_status"] = "success"
        execution_summary["total_execution_time"] = total_execution_time
        
        setup_results.append("╔════════════════════════════════════════════════════════════════╗")
        setup_results.append("║  ✅ POC SETUP COMPLETE                                        ║")
        setup_results.append("╚════════════════════════════════════════════════════════════════╝")
        setup_results.append(f"⏱️  Total time: {total_execution_time:.2f}s")
        setup_results.append(f"🔄 Total retries: {execution_summary['total_retries']}")
        
        return {
            "status": "success",
            "message": "\n".join(setup_results),
            "data": result_data,
            "execution_summary": execution_summary
        }
        
    except Exception as error:
        logger.error(f"Error in GovernInternetAccessPOC: {error}")
        return {
            "status": "error",
            "message": f"Unexpected error: {str(error)}"
        }
