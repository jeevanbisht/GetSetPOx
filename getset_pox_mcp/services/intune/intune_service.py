"""
Intune Service Implementation.

This service provides Microsoft Intune device management and app deployment tools
via Microsoft Graph API.

Dependencies:
- httpx: For async HTTP requests
- getset_pox_mcp.authentication.middleware: For authentication token management
"""

from typing import Any, Optional, List
from getset_pox_mcp.logging_config import get_logger
from getset_pox_mcp.authentication.middleware import get_auth_middleware
import httpx
import json
import asyncio

logger = get_logger(__name__)

async def IN_listIntuneManagedDevices(top: int = 10) -> dict[str, Any]:
    """
    List all managed devices in Microsoft Intune.
    
    Args:
        top: Number of devices to return (default: 10)
        
    Returns:
        Dictionary with list of managed devices and their details.
    """
    logger.info(f"IN_listIntuneManagedDevices called with top={top}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/beta/deviceManagement/managedDevices?$top={top}",
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
        
        if not data.get("value") or len(data["value"]) == 0:
            return {"status": "success", "message": "No managed devices found.", "devices": []}
        
        devices = []
        for idx, device in enumerate(data["value"], 1):
            device_info = {
                "index": idx,
                "deviceName": device.get("deviceName", "Unknown"),
                "operatingSystem": device.get("operatingSystem", "N/A"),
                "userDisplayName": device.get("userDisplayName", "N/A"),
                "id": device.get("id")
            }
            devices.append(device_info)
        
        device_list = "\n\n".join([
            f"{d['index']}. {d['deviceName']}\n   OS: {d['operatingSystem']}\n   User: {d['userDisplayName']}\n   ID: {d['id']}"
            for d in devices
        ])
        
        return {
            "status": "success",
            "message": f"Found {len(devices)} managed devices:\n\n{device_list}",
            "count": len(devices),
            "devices": devices
        }
    except Exception as error:
        logger.error(f"Error listing managed devices: {error}")
        return {"status": "error", "message": f"Error listing managed devices: {str(error)}"}

async def IN_getManagedDeviceDetails(deviceId: str) -> dict[str, Any]:
    """
    Get detailed information about a specific managed device.
    
    Args:
        deviceId: The ID of the managed device
        
    Returns:
        Dictionary with detailed device information.
    """
    logger.info(f"IN_getManagedDeviceDetails called for device: {deviceId}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.microsoft.com/beta/deviceManagement/managedDevices/{deviceId}",
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            device = response.json()
        
        details_list = [
            f"Device Name: {device.get('deviceName', 'Unknown')}",
            f"Operating System: {device.get('operatingSystem', 'N/A')}",
            f"OS Version: {device.get('osVersion', 'N/A')}",
            f"User: {device.get('userDisplayName', 'N/A')} ({device.get('userPrincipalName', 'N/A')})",
            f"Compliance State: {device.get('complianceState', 'N/A')}",
            f"Enrollment Date: {device.get('enrolledDateTime', 'N/A')}",
            f"Last Sync: {device.get('lastSyncDateTime', 'N/A')}",
            f"Management State: {device.get('managementState', 'N/A')}",
            f"Serial Number: {device.get('serialNumber', 'N/A')}",
            f"Model: {device.get('model', 'N/A')}",
            f"Manufacturer: {device.get('manufacturer', 'N/A')}",
            f"ID: {device.get('id')}"
        ]
        
        details = "\n".join(details_list)
        
        return {
            "status": "success",
            "message": f"Managed Device Details:\n\n{details}",
            "device": device
        }
    except Exception as error:
        logger.error(f"Error getting device details: {error}")
        return {"status": "error", "message": f"Error getting device details: {str(error)}"}

async def IN_listDeviceCompliancePolicies() -> dict[str, Any]:
    """
    List all device compliance policies in Microsoft Intune.
    
    Returns:
        Dictionary with list of compliance policies.
    """
    logger.info("IN_listDeviceCompliancePolicies called")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://graph.microsoft.com/beta/deviceManagement/deviceCompliancePolicies",
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
        
        if not data.get("value") or len(data["value"]) == 0:
            return {"status": "success", "message": "No device compliance policies found.", "policies": []}
        
        policies = []
        for idx, policy in enumerate(data["value"], 1):
            odata_type = policy.get("@odata.type", "")
            platform = odata_type.split(".")[-1] if odata_type else "Unknown"
            
            policy_info = {
                "index": idx,
                "displayName": policy.get("displayName", "Unnamed Policy"),
                "platform": platform,
                "description": policy.get("description", "No description"),
                "id": policy.get("id")
            }
            policies.append(policy_info)
        
        policy_list = "\n\n".join([
            f"{p['index']}. {p['displayName']}\n   Platform: {p['platform']}\n   Description: {p['description']}\n   ID: {p['id']}"
            for p in policies
        ])
        
        return {
            "status": "success",
            "message": f"Found {len(policies)} compliance policies:\n\n{policy_list}",
            "count": len(policies),
            "policies": policies
        }
    except Exception as error:
        logger.error(f"Error listing compliance policies: {error}")
        return {"status": "error", "message": f"Error listing compliance policies: {str(error)}"}

async def IN_listDeviceConfigurationProfiles() -> dict[str, Any]:
    """
    List all device configuration profiles in Microsoft Intune.
    
    Returns:
        Dictionary with list of configuration profiles.
    """
    logger.info("IN_listDeviceConfigurationProfiles called")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://graph.microsoft.com/beta/deviceManagement/deviceConfigurations",
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
        
        if not data.get("value") or len(data["value"]) == 0:
            return {"status": "success", "message": "No device configuration profiles found.", "profiles": []}
        
        profiles = []
        for idx, profile in enumerate(data["value"], 1):
            odata_type = profile.get("@odata.type", "")
            platform = odata_type.split(".")[-1] if odata_type else "Unknown"
            
            profile_info = {
                "index": idx,
                "displayName": profile.get("displayName", "Unnamed Profile"),
                "platform": platform,
                "description": profile.get("description", "No description"),
                "id": profile.get("id")
            }
            profiles.append(profile_info)
        
        profile_list = "\n\n".join([
            f"{p['index']}. {p['displayName']}\n   Platform: {p['platform']}\n   Description: {p['description']}\n   ID: {p['id']}"
            for p in profiles
        ])
        
        return {
            "status": "success",
            "message": f"Found {len(profiles)} configuration profiles:\n\n{profile_list}",
            "count": len(profiles),
            "profiles": profiles
        }
    except Exception as error:
        logger.error(f"Error listing configuration profiles: {error}")
        return {"status": "error", "message": f"Error listing configuration profiles: {str(error)}"}

async def IN_syncManagedDevice(deviceId: str) -> dict[str, Any]:
    """
    Trigger a sync for a specific managed device.
    
    Args:
        deviceId: The ID of the managed device to sync
        
    Returns:
        Dictionary with sync operation result.
    """
    logger.info(f"IN_syncManagedDevice called for device: {deviceId}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://graph.microsoft.com/beta/deviceManagement/managedDevices/{deviceId}/syncDevice",
                headers=headers,
                json={},
                timeout=60.0
            )
            response.raise_for_status()
        
        return {
            "status": "success",
            "message": f"✅ Sync command sent successfully to device: {deviceId}\n\nNote: The device will sync when it next checks in with Intune.",
            "deviceId": deviceId
        }
    except Exception as error:
        logger.error(f"Error syncing device: {error}")
        return {"status": "error", "message": f"Error syncing device: {str(error)}"}

async def _prepGSAWinClient_core(
    displayName: str,
    description: str,
    publisher: str,
    sasUrl: Optional[str],
    progress_messages: list
) -> dict[str, Any]:
    """
    Core implementation of GSA Client installer upload with real-time progress reporting.
    
    This internal function contains all the logic for downloading and uploading the GSA client
    to Intune. It emits progress messages through the provided progress_messages list.
    
    IMPORTANT: This is complex, tested logic - DO NOT MODIFY the core workflow.
    Only adapted for async/await pattern with auth_middleware.
    
    Args:
        displayName: Display name for the app in Intune
        description: Description of the app
        publisher: Publisher name
        sasUrl: Optional custom SAS URL for the installer
        progress_messages: List to collect progress messages
        
    Returns:
        Dictionary with detailed deployment results including app ID and status.
    """
    import base64
    import hashlib
    import zipfile
    import io
    import time
    import re
    import tempfile
    from pathlib import Path
    
    auth_middleware = get_auth_middleware()
    token = await auth_middleware.get_valid_token()
    
    if not token:
        raise Exception("Authentication token not available. Authentication may be disabled or failed.")
    
    temp_path = None
    
    try:
        # STEP 1: Download the .intunewin package
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 1: Downloading .intunewin Package                       ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        default_sas_url = "https://jblabintune.blob.core.windows.net/testclient/GlobalSecureAccessClient.intunewin?sp=r&st=2025-11-17T00:05:00Z&se=2027-02-11T08:20:00Z&spr=https&sv=2024-11-04&sr=b&sig=Qf9h5RnujKMNA8UdlNueQg%2BBdtDXlzxnbAiDLxxJwLs%3D"
        download_url = sasUrl or default_sas_url
        
        progress_messages.append(f"📥 Downloading from: {download_url[:80]}...")
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            download_response = await client.get(download_url)
            download_response.raise_for_status()
        
        file_buffer = download_response.content
        file_size = len(file_buffer)
        file_size_mb = file_size / (1024 * 1024)
        file_name = "GlobalSecureAccessClient.intunewin"
        
        # Calculate file hash
        file_hash = hashlib.sha256(file_buffer).hexdigest()
        
        progress_messages.append(f"✅ Download complete")
        progress_messages.append(f"   Size: {file_size_mb:.2f} MB ({file_size} bytes)")
        progress_messages.append(f"   SHA256: {file_hash}")
        
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".intunewin") as temp_file:
            temp_path = temp_file.name
            temp_file.write(file_buffer)
        
        progress_messages.append(f"   Temp file: {temp_path}")
        
        # STEP 2: Create Win32LobApp in Intune
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 2: Creating Win32 LOB App in Intune                     ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        app_body = {
            "@odata.type": "#microsoft.graph.win32LobApp",
            "displayName": displayName,
            "description": description,
            "publisher": publisher,
            "fileName": file_name,
            "isFeatured": False,
            "privacyInformationUrl": "https://learn.microsoft.com/en-us/entra/global-secure-access/",
            "informationUrl": "https://learn.microsoft.com/en-us/entra/global-secure-access/how-to-install-windows-client",
            "developer": "Microsoft Corporation",
            "notes": "Global Secure Access client for Windows. Automated upload via MCP.",
            "installCommandLine": "GlobalSecureAccessClient.exe /quiet /norestart",
            "uninstallCommandLine": "GlobalSecureAccessClient.exe /uninstall /quiet /norestart",
            "setupFilePath": "GlobalSecureAccessClient.exe",
            "minimumSupportedOperatingSystem": {
                "@odata.type": "#microsoft.graph.windowsMinimumOperatingSystem",
                "v10_1809": True
            },
            "installExperience": {
                "@odata.type": "#microsoft.graph.win32LobAppInstallExperience",
                "runAsAccount": "system",
                "deviceRestartBehavior": "suppress"
            },
            "detectionRules": [
                {
                    "@odata.type": "#microsoft.graph.win32LobAppFileSystemDetection",
                    "path": "%ProgramFiles%\\Global Secure Access Client",
                    "fileOrFolderName": "GlobalSecureAccessClient.exe",
                    "check32BitOn64System": False,
                    "detectionType": "exists",
                    "operator": "notConfigured"
                }
            ],
            "requirementRules": [
                {
                    "@odata.type": "#microsoft.graph.win32LobAppPowerShellScriptRequirement",
                    "displayName": "Windows 10 1809+",
                    "enforceSignatureCheck": False,
                    "runAs32Bit": False,
                    "detectionType": "string",
                    "scriptContent": base64.b64encode(b"[System.Environment]::OSVersion.Version.Build").decode('utf-8')
                }
            ],
            "returnCodes": [
                {"returnCode": 0, "type": "success"},
                {"returnCode": 1707, "type": "success"},
                {"returnCode": 3010, "type": "softReboot"},
                {"returnCode": 1641, "type": "hardReboot"},
                {"returnCode": 1618, "type": "retry"}
            ]
        }
        
        progress_messages.append(f"📱 Creating app: {displayName}")
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            app_response = await client.post(
                "https://graph.microsoft.com/beta/deviceAppManagement/mobileApps",
                headers=headers,
                json=app_body
            )
            app_response.raise_for_status()
            app_data = app_response.json()
        
        app_id = app_data["id"]
        progress_messages.append(f"✅ App created successfully")
        progress_messages.append(f"   App ID: {app_id}")
        progress_messages.append(f"   Display Name: {app_data.get('displayName')}")
        
        # STEP 3: Create Content Version
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 3: Creating Content Version                             ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        progress_messages.append(f"📦 Creating content version for app {app_id}...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            content_version_response = await client.post(
                f"https://graph.microsoft.com/beta/deviceAppManagement/mobileApps/{app_id}/microsoft.graph.win32LobApp/contentVersions",
                headers=headers,
                json={}
            )
            content_version_response.raise_for_status()
            content_version_data = content_version_response.json()
        
        content_version_id = content_version_data["id"]
        progress_messages.append(f"✅ Content version created")
        progress_messages.append(f"   Version ID: {content_version_id}")
        
        # STEP 4: Extract metadata and create file entry
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 4: Creating File Placeholder                            ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        progress_messages.append(f"📄 Extracting file metadata from Detection.xml...")
        
        # Extract metadata from .intunewin file
        with zipfile.ZipFile(io.BytesIO(file_buffer), 'r') as zip_file:
            detection_xml = zip_file.read('IntuneWinPackage/Metadata/Detection.xml').decode('utf-8')
            encrypted_content = zip_file.read('IntuneWinPackage/Contents/IntunePackage.intunewin')
        
        # Parse unencrypted size from XML
        unencrypted_match = re.search(r'<UnencryptedContentSize>(\d+)</UnencryptedContentSize>', detection_xml)
        unencrypted_size = int(unencrypted_match.group(1)) if unencrypted_match else file_size
        
        encrypted_file_size = len(encrypted_content)
        
        progress_messages.append(f"   Unencrypted size from XML: {unencrypted_size / (1024 * 1024):.2f} MB ({unencrypted_size} bytes)")
        progress_messages.append(f"   Encrypted file size: {encrypted_file_size / (1024 * 1024):.2f} MB ({encrypted_file_size} bytes)")
        progress_messages.append(f"   Wrapper size: {file_size_mb:.2f} MB ({file_size} bytes)")
        
        file_body = {
            "@odata.type": "#microsoft.graph.mobileAppContentFile",
            "name": file_name,
            "size": unencrypted_size,
            "sizeEncrypted": encrypted_file_size,
            "manifest": None,
            "isDependency": False
        }
        
        progress_messages.append(f"📄 Creating file entry: {file_name}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            file_response = await client.post(
                f"https://graph.microsoft.com/beta/deviceAppManagement/mobileApps/{app_id}/microsoft.graph.win32LobApp/contentVersions/{content_version_id}/files",
                headers=headers,
                json=file_body
            )
            file_response.raise_for_status()
            file_data = file_response.json()
        
        file_id = file_data["id"]
        azure_storage_uri = file_data.get("azureStorageUri")
        
        progress_messages.append(f"✅ File placeholder created")
        progress_messages.append(f"   File ID: {file_id}")
        progress_messages.append(f"   Azure Storage URI: {'Received' if azure_storage_uri else 'Pending'}")
        
        # STEP 5: Wait for Azure Storage URI
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 5: Waiting for Azure Storage URI                        ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        upload_uri = azure_storage_uri
        attempts = 0
        max_attempts = 30
        
        while not upload_uri and attempts < max_attempts:
            progress_messages.append(f"⏳ Waiting for upload URI... (attempt {attempts + 1}/{max_attempts})")
            await asyncio.sleep(2)
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                file_status_response = await client.get(
                    f"https://graph.microsoft.com/beta/deviceAppManagement/mobileApps/{app_id}/microsoft.graph.win32LobApp/contentVersions/{content_version_id}/files/{file_id}",
                    headers=headers
                )
                file_status_response.raise_for_status()
                file_status = file_status_response.json()
            
            upload_uri = file_status.get("azureStorageUri")
            attempts += 1
        
        if not upload_uri:
            raise Exception(f"Failed to get Azure Storage URI after {max_attempts} attempts")
        
        progress_messages.append(f"✅ Upload URI received")
        progress_messages.append(f"   URI: {upload_uri[:80]}...")
        
        # STEP 6: Upload file to Azure Storage (chunked)
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 6: Uploading File to Azure Storage                      ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        progress_messages.append(f"☁️  Uploading {file_size_mb:.2f} MB to Azure Storage...")
        progress_messages.append(f"   This may take several minutes...")
        progress_messages.append(f"   ⚠️  Note: Uploading ENCRYPTED file - Intune decrypts server-side!")
        
        # Calculate hash of encrypted content
        encrypted_hash = hashlib.sha256(encrypted_content).hexdigest()
        progress_messages.append(f"   📝 Encrypted content SHA256: {encrypted_hash}")
        
        # Upload in 6MB chunks
        chunk_size = 6 * 1024 * 1024
        total_chunks = (len(encrypted_content) + chunk_size - 1) // chunk_size
        progress_messages.append(f"   📦 Splitting into {total_chunks} chunks of {chunk_size / (1024 * 1024):.2f} MB each...")
        
        block_ids = []
        
        for i in range(total_chunks):
            start = i * chunk_size
            end = min(start + chunk_size, len(encrypted_content))
            chunk = encrypted_content[start:end]
            
            # Create block ID (must be base64 encoded)
            block_id = base64.b64encode(str(i).zfill(5).encode()).decode()
            block_ids.append(block_id)
            
            # Upload chunk
            chunk_uri = f"{upload_uri}&comp=block&blockid={block_id}"
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                chunk_response = await client.put(
                    chunk_uri,
                    content=chunk,
                    headers={"Content-Type": "application/octet-stream"}
                )
                chunk_response.raise_for_status()
            
            # Report progress for every chunk or at specific intervals
            if total_chunks <= 10 or (i + 1) % max(1, total_chunks // 10) == 0 or i == total_chunks - 1:
                progress_messages.append(f"   ⏳ Uploaded {i + 1}/{total_chunks} chunks ({((i + 1) / total_chunks * 100):.1f}%)")
        
        progress_messages.append(f"   ✅ All chunks uploaded successfully")
        
        # Commit block list
        progress_messages.append(f"   🔗 Committing block list...")
        block_list_xml = '<?xml version="1.0" encoding="utf-8"?><BlockList>' + \
            ''.join([f'<Latest>{bid}</Latest>' for bid in block_ids]) + \
            '</BlockList>'
        
        commit_uri = f"{upload_uri}&comp=blocklist"
        async with httpx.AsyncClient(timeout=60.0) as client:
            commit_response = await client.put(
                commit_uri,
                content=block_list_xml,
                headers={"Content-Type": "application/xml"}
            )
            commit_response.raise_for_status()
        
        progress_messages.append(f"✅ Upload to Azure Storage complete (chunked upload with {total_chunks} blocks)")
        
        # STEP 7: Commit the file
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 7: Committing File Upload                               ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        progress_messages.append(f"🔒 Committing file upload...")
        progress_messages.append(f"   📦 Extracting encryption metadata from .intunewin package...")
        
        # Extract encryption info from Detection.xml
        enc_key_match = re.search(r'<EncryptionKey>\s*([^<]+?)\s*</EncryptionKey>', detection_xml, re.IGNORECASE | re.DOTALL)
        mac_key_match = re.search(r'<MacKey>\s*([^<]+?)\s*</MacKey>', detection_xml, re.IGNORECASE | re.DOTALL)
        iv_match = re.search(r'<InitializationVector>\s*([^<]+?)\s*</InitializationVector>', detection_xml, re.IGNORECASE | re.DOTALL)
        mac_match = re.search(r'<Mac>\s*([^<]+?)\s*</Mac>', detection_xml, re.IGNORECASE | re.DOTALL)
        profile_match = re.search(r'<ProfileIdentifier>\s*([^<]+?)\s*</ProfileIdentifier>', detection_xml, re.IGNORECASE | re.DOTALL)
        digest_match = re.search(r'<FileDigest>\s*([^<]+?)\s*</FileDigest>', detection_xml, re.IGNORECASE | re.DOTALL)
        algo_match = re.search(r'<FileDigestAlgorithm>\s*([^<]+?)\s*</FileDigestAlgorithm>', detection_xml, re.IGNORECASE | re.DOTALL)
        
        if not all([enc_key_match, mac_key_match, iv_match, mac_match]):
            raise Exception("Could not parse all required encryption fields from Detection.xml")
        
        encryption_info = {
            "encryptionKey": enc_key_match.group(1).strip(),
            "macKey": mac_key_match.group(1).strip(),
            "initializationVector": iv_match.group(1).strip(),
            "mac": mac_match.group(1).strip(),
            "profileIdentifier": profile_match.group(1).strip() if profile_match else "ProfileVersion1",
            "fileDigest": digest_match.group(1).strip() if digest_match else None,
            "fileDigestAlgorithm": algo_match.group(1).strip() if algo_match else "SHA256"
        }
        
        progress_messages.append(f"   ✅ Successfully extracted encryption metadata from package")
        
        commit_body = {"fileEncryptionInfo": encryption_info}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            commit_file_response = await client.post(
                f"https://graph.microsoft.com/beta/deviceAppManagement/mobileApps/{app_id}/microsoft.graph.win32LobApp/contentVersions/{content_version_id}/files/{file_id}/commit",
                headers=headers,
                json=commit_body
            )
            commit_file_response.raise_for_status()
        
        progress_messages.append(f"✅ File committed with extracted encryption metadata")
        
        # STEP 8: Wait for processing
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 8: Waiting for Processing Completion                    ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        processing_complete = False
        attempts = 0
        max_processing_attempts = 60
        
        while not processing_complete and attempts < max_processing_attempts:
            await asyncio.sleep(3)
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                file_status_response = await client.get(
                    f"https://graph.microsoft.com/beta/deviceAppManagement/mobileApps/{app_id}/microsoft.graph.win32LobApp/contentVersions/{content_version_id}/files/{file_id}",
                    headers=headers
                )
                file_status_response.raise_for_status()
                file_status = file_status_response.json()
            
            upload_state = file_status.get("uploadState")
            
            # Report every 5 attempts or on state change
            if attempts % 5 == 0 or attempts == 0:
                progress_messages.append(f"⏳ Processing... State: {upload_state} (attempt {attempts + 1}/{max_processing_attempts})")
            
            if upload_state == "commitFileSuccess":
                processing_complete = True
            elif upload_state == "commitFileFailed":
                progress_messages.append(f"")
                progress_messages.append(f"   ❌ Commit failed on server. File status: {file_status}")
                raise Exception(f"File commit failed on server side. Upload state: {upload_state}")
            
            attempts += 1
        
        if not processing_complete:
            progress_messages.append(f"⚠️  Processing timeout - app may still be processing")
        else:
            progress_messages.append(f"✅ Processing complete!")
        
        # STEP 9: Finalize content version
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  STEP 9: Finalizing Content Version                           ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        
        progress_messages.append(f"🎯 Setting committed content version on app...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            finalize_response = await client.patch(
                f"https://graph.microsoft.com/beta/deviceAppManagement/mobileApps/{app_id}",
                headers=headers,
                json={
                    "@odata.type": "#microsoft.graph.win32LobApp",
                    "committedContentVersion": content_version_id
                }
            )
            finalize_response.raise_for_status()
        
        progress_messages.append(f"✅ Content version finalized")
        
        # SUCCESS SUMMARY
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  🎉 DEPLOYMENT COMPLETE!                                       ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        progress_messages.append("")
        progress_messages.append("📱 Application Details:")
        progress_messages.append(f"   App ID: {app_id}")
        progress_messages.append(f"   Display Name: {displayName}")
        progress_messages.append(f"   Publisher: {publisher}")
        progress_messages.append(f"   File: {file_name} ({file_size_mb:.2f} MB)")
        progress_messages.append(f"   Content Version: {content_version_id}")
        progress_messages.append("")
        progress_messages.append("✅ Next Steps:")
        progress_messages.append("   1. Assign the app to groups in Intune portal")
        progress_messages.append("   2. Configure deployment settings (Required/Available)")
        progress_messages.append("   3. Monitor deployment status in Intune")
        
        # Cleanup
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
                progress_messages.append("")
                progress_messages.append("🧹 Temporary file cleaned up")
            except Exception as cleanup_error:
                progress_messages.append("")
                progress_messages.append(f"⚠️  Could not remove temp file: {cleanup_error}")
        
        return {
            "status": "success",
            "app_id": app_id,
            "content_version_id": content_version_id,
            "display_name": displayName
        }
        
    except Exception as error:
        progress_messages.append("")
        progress_messages.append("╔════════════════════════════════════════════════════════════════╗")
        progress_messages.append("║  ❌ ERROR OCCURRED                                             ║")
        progress_messages.append("╚════════════════════════════════════════════════════════════════╝")
        progress_messages.append(f"Error: {str(error)}")
        
        # Cleanup on error
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
                progress_messages.append("")
                progress_messages.append("🧹 Temporary file cleaned up")
            except:
                pass
        
        logger.error(f"Error in _prepGSAWinClient_core: {error}")
        raise

async def IN_prepGSAWinClient(
    displayName: str = "Global Secure Access Client",
    description: str = "Microsoft Global Secure Access Windows client for secure network connectivity",
    publisher: str = "Microsoft",
    sasUrl: Optional[str] = None
) -> dict[str, Any]:
    """
    Prepares installation of the Global Secure Access (GSA) Windows Client for Microsoft Intune.
    
    Downloads the GSA Windows Client installer and uploads it to Microsoft Intune using 
    Microsoft Graph API. Handles all deployment steps: app creation, content version 
    management, Azure Storage upload, and content commit. All progress messages are 
    collected and included in the final result.
    
    This tool automates the complete workflow for deploying the Global Secure Access 
    Windows Client through Intune, eliminating manual upload processes and ensuring 
    proper configuration for enterprise deployment.
    
    Args:
        displayName: Display name for the app in Intune (default: "Global Secure Access Client")
        description: Description of the GSA Windows Client app
        publisher: Publisher name (default: "Microsoft")
        sasUrl: Optional custom SAS URL for the installer package
        
    Returns:
        Dictionary with detailed deployment results including app ID, content version, and status.
        All progress messages from the deployment process are included in the result.
    """
    logger.info(f"IN_prepGSAWinClient called: {displayName}")
    
    auth_middleware = get_auth_middleware()
    token = await auth_middleware.get_valid_token()
    
    if not token:
        return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
    
    progress_messages = []
    
    try:
        result = await _prepGSAWinClient_core(
            displayName=displayName,
            description=description,
            publisher=publisher,
            sasUrl=sasUrl,
            progress_messages=progress_messages
        )
        
        # Add full message text to result
        result["message"] = "\n".join(progress_messages)
        return result
        
    except Exception as error:
        error_result = {
            "status": "error",
            "message": "\n".join(progress_messages + [f"\n❌ ERROR: {str(error)}"]),
            "error": str(error)
        }
        return error_result

async def IN_intuneAppAssignment(
    appId: str,
    groupIds: List[str],
    intent: str = "required",
    notificationSettings: str = "showAll",
    restartGracePeriod: int = 1440,
    deliveryOptimizationPriority: str = "notConfigured"
) -> dict[str, Any]:
    """
    Assign device groups to Intune Win32 applications with configurable deployment settings.
    
    Args:
        appId: The Win32 LOB App ID to assign groups to
        groupIds: Array of Entra ID group object IDs to assign the app to
        intent: Deployment intent: 'required', 'available', or 'uninstall'
        notificationSettings: Notification display level: 'showAll', 'showReboot', or 'hideAll'
        restartGracePeriod: Grace period in minutes before forcing restart (default: 1440)
        deliveryOptimizationPriority: Delivery optimization priority: 'notConfigured' or 'foreground'
        
    Returns:
        Dictionary with assignment results and details.
    """
    logger.info(f"IN_intuneAppAssignment called for app: {appId}")
    
    results = []
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available."}
        
        results.append("╔════════════════════════════════════════════════════════════════╗")
        results.append("║  Intune App Assignment                                        ║")
        results.append("╚════════════════════════════════════════════════════════════════╝")
        results.append("")
        
        # Validate inputs
        if len(groupIds) == 0:
            raise Exception("At least one group ID must be provided")
        
        if len(groupIds) > 50:
            results.append("⚠️  Warning: Assigning to more than 50 groups may take a while")
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        async with httpx.AsyncClient() as client:
            # STEP 1: Get app details
            results.append("📋 Step 1: Retrieving and Validating App Details")
            results.append(f"   App ID: {appId}")
            results.append("")
            
            app_response = await client.get(
                f"https://graph.microsoft.com/beta/deviceAppManagement/mobileApps/{appId}",
                headers=headers,
                timeout=30.0
            )
            app_response.raise_for_status()
            app_details = app_response.json()
            
            results.append("✅ App found:")
            results.append(f"   Display Name: {app_details.get('displayName', 'N/A')}")
            results.append(f"   Publisher: {app_details.get('publisher', 'N/A')}")
            results.append(f"   Type: {app_details.get('@odata.type', 'N/A')}")
            
            if app_details.get("committedContentVersion"):
                results.append(f"   ✅ Committed Content Version: {app_details['committedContentVersion']}")
            else:
                results.append(f"   ⚠️  WARNING: No committed content version!")
            
            results.append("")
            
            # STEP 2: Check existing assignments
            results.append("📋 Step 2: Checking Existing Assignments")
            
            try:
                assignments_response = await client.get(
                    f"https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps/{appId}/assignments",
                    headers=headers,
                    timeout=30.0
                )
                assignments_response.raise_for_status()
                existing_assignments = assignments_response.json().get("value", [])
                results.append(f"   Found {len(existing_assignments)} existing assignment(s)")
            except:
                results.append(f"   ⚠️  Could not retrieve existing assignments")
            
            results.append("")
            
            # STEP 3: Create assignments
            results.append("📋 Step 3: Creating Assignment Configuration")
            results.append(f"   Deployment Intent: {intent}")
            results.append(f"   Number of Groups: {len(groupIds)}")
            results.append(f"   Notification Settings: {notificationSettings}")
            results.append("")
            
            # STEP 4: Assign groups
            results.append("📋 Step 4: Assigning Groups to Application")
            results.append("")
            
            successful_assignments = []
            failed_assignments = []
            
            for i, group_id in enumerate(groupIds):
                assignment = {
                    "@odata.type": "#microsoft.graph.mobileAppAssignment",
                    "intent": intent,
                    "target": {
                        "@odata.type": "#microsoft.graph.groupAssignmentTarget",
                        "groupId": group_id
                    },
                    "settings": {
                        "@odata.type": "#microsoft.graph.win32LobAppAssignmentSettings",
                        "notifications": notificationSettings,
                        "restartSettings": {
                            "gracePeriodInMinutes": restartGracePeriod,
                            "countdownDisplayBeforeRestartInMinutes": 15,
                            "restartNotificationSnoozeDurationInMinutes": 240
                        },
                        "deliveryOptimizationPriority": deliveryOptimizationPriority
                    }
                }
                
                if intent == "required":
                    assignment["settings"]["installTimeSettings"] = {
                        "useLocalTime": False,
                        "deadlineDateTime": None
                    }
                
                try:
                    results.append(f"   [{i + 1}/{len(groupIds)}] Assigning group: {group_id}")
                    
                    assignment_response = await client.post(
                        f"https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps/{appId}/assignments",
                        headers=headers,
                        json=assignment,
                        timeout=30.0
                    )
                    assignment_response.raise_for_status()
                    assignment_data = assignment_response.json()
                    
                    successful_assignments.append({
                        "groupId": group_id,
                        "assignmentId": assignment_data["id"],
                        "intent": intent
                    })
                    
                    results.append(f"      ✅ Assignment created: {assignment_data['id']}")
                    
                    if i < len(groupIds) - 1:
                        await asyncio.sleep(0.2)
                except Exception as error:
                    error_msg = str(error)
                    results.append(f"      ❌ Failed: {error_msg}")
                    
                    failed_assignments.append({
                        "groupId": group_id,
                        "error": error_msg
                    })
            
            results.append("")
            results.append("╔════════════════════════════════════════════════════════════════╗")
            results.append("║  ASSIGNMENT SUMMARY                                            ║")
            results.append("╚════════════════════════════════════════════════════════════════╝")
            results.append("")
            results.append(f"📊 Assignment Results:")
            results.append(f"   Successfully assigned: {len(successful_assignments)}")
            results.append(f"   Failed: {len(failed_assignments)}")
            
            response_data = {
                "success": len(failed_assignments) == 0,
                "app": {
                    "id": appId,
                    "displayName": app_details.get("displayName"),
                    "publisher": app_details.get("publisher")
                },
                "assignment": {
                    "intent": intent,
                    "notificationSettings": notificationSettings,
                    "totalGroups": len(groupIds),
                    "successfulAssignments": len(successful_assignments),
                    "failedAssignments": len(failed_assignments)
                },
                "assignments": successful_assignments
            }
            
            if failed_assignments:
                response_data["errors"] = failed_assignments
            
            return {
                "status": "success" if len(failed_assignments) == 0 else "partial",
                "message": "\n".join(results),
                "data": response_data
            }
        
    except Exception as error:
        results.append("")
        results.append("╔════════════════════════════════════════════════════════════════╗")
        results.append("║  ❌ ERROR OCCURRED                                             ║")
        results.append("╚════════════════════════════════════════════════════════════════╝")
        results.append(f"Error: {str(error)}")
        
        logger.error(f"Error in IN_intuneAppAssignment: {error}")
        return {
            "status": "error",
            "message": "\n".join(results),
            "error": str(error)
        }
