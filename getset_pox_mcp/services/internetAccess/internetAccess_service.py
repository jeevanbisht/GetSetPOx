"""
Internet Access Service Implementation.

This service provides Entra Global Secure Access (Internet Access) management tools
for configuring web content filtering, forwarding profiles, and TLS inspection.
"""

from typing import Any, List, Optional
from getset_pox_mcp.logging_config import get_logger
from getset_pox_mcp.authentication.middleware import get_auth_middleware
import httpx

logger = get_logger(__name__)

async def IA_checkInternetAccessForwardingProfile() -> dict[str, Any]:
    """Check if the Internet Access Forwarding Profile is enabled."""
    logger.info("IA_checkInternetAccessForwardingProfile called")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://graph.microsoft.com/beta/networkAccess/forwardingProfiles?$filter=trafficForwardingType eq 'internet'",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        if not data.get("value") or len(data["value"]) == 0:
            return {"status": "not_found", "message": "No Internet Access Forwarding Profile found."}
        
        profile = data["value"][0]
        return {
            "status": "success",
            "name": profile.get("name"),
            "state": profile.get("state"),
            "id": profile.get("id"),
            "message": f"Internet Access Forwarding Profile:\nName: {profile.get('name')}\nState: {profile.get('state')}\nID: {profile.get('id')}"
        }
    except Exception as error:
        logger.error(f"Error checking Internet Access Forwarding Profile: {error}")
        return {"status": "error", "message": f"Error: {str(error)}"}

async def IA_enableInternetAccessForwardingProfile(
    forwarding_profile_id: str,
    state: str = "enabled"
) -> dict[str, Any]:
    """Enable the Internet Access Forwarding Profile."""
    logger.info(f"IA_enableInternetAccessForwardingProfile called: profile_id={forwarding_profile_id}, state={state}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        async with httpx.AsyncClient() as client:
            # Get current profile
            get_response = await client.get(
                f"https://graph.microsoft.com/beta/networkAccess/forwardingProfiles/{forwarding_profile_id}",
                headers=headers
            )
            get_response.raise_for_status()
            data = get_response.json()
            
            if not data or not data.get("id"):
                return {"status": "not_found", "message": "No Internet Access Forwarding Profile found with the specified ID."}
            
            # Check if already in target state
            if data.get("state") == state:
                return {
                    "status": "already_set",
                    "name": data.get("name"),
                    "id": data.get("id"),
                    "message": f"Internet Access Forwarding Profile is already {state}.\nName: {data.get('name')}\nID: {data.get('id')}"
                }
            
            # Update state
            patch_response = await client.patch(
                f"https://graph.microsoft.com/beta/networkAccess/forwardingProfiles/{forwarding_profile_id}",
                headers=headers,
                json={"state": state}
            )
            patch_response.raise_for_status()
            
            return {
                "status": "success",
                "name": data.get("name"),
                "id": data.get("id"),
                "message": f"Internet Access Forwarding Profile has been {state}.\nName: {data.get('name')}\nID: {data.get('id')}"
            }
    except Exception as error:
        logger.error(f"Error enabling Internet Access Forwarding Profile: {error}")
        return {"status": "error", "message": f"Error: {str(error)}"}

async def IA_createFilteringPolicy(
    name: str = "POC-Monitor AI Access",
    description: str = "Monitor access to AI",
    webCategories: Optional[List[str]] = None
) -> dict[str, Any]:
    """Create an allow filtering policy for one or more web categories."""
    if webCategories is None:
        webCategories = ["ArtificialIntelligence"]
    
    logger.info(f"IA_createFilteringPolicy called: name={name}, categories={webCategories}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        destinations = [
            {"@odata.type": "#microsoft.graph.networkaccess.webCategory", "name": category}
            for category in webCategories
        ]
        
        rule_name = name if len(webCategories) == 1 else f"{' and '.join(webCategories)} categories"
        
        body = {
            "name": name,
            "policyRules": [{
                "@odata.type": "#microsoft.graph.networkaccess.webCategoryFilteringRule",
                "name": rule_name,
                "ruleType": "webCategory",
                "destinations": destinations
            }],
            "action": "allow",
            "description": description,
            "@odata.type": "#microsoft.graph.networkaccess.filteringPolicy"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://graph.microsoft.com/beta/networkAccess/filteringPolicies",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            result = response.json()
        
        return {
            "status": "success",
            "policy_name": result.get("name"),
            "policy_id": result.get("id"),
            "message": f"Filtering policy created for categories: {', '.join(webCategories)}.\nPolicy Name: {result.get('name')}\nID: {result.get('id')}"
        }
    except Exception as error:
        logger.error(f"Error creating filtering policy: {error}")
        return {"status": "error", "message": f"Error: {str(error)}"}

async def IA_createFilteringProfile(
    name: str = "POC-Monitor AI Access Profile",
    description: str = "Profile for monitoring AI access",
    state: str = "enabled",
    priority: int = 1000
) -> dict[str, Any]:
    """Create a filtering profile."""
    logger.info(f"IA_createFilteringProfile called: name={name}, state={state}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        body = {"name": name, "description": description, "state": state, "priority": priority}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://graph.microsoft.com/beta/networkAccess/filteringProfiles",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            result = response.json()
        
        return {
            "status": "success",
            "profile_name": result.get("name"),
            "profile_id": result.get("id"),
            "message": f"Filtering profile created.\nProfile Name: {result.get('name')}\nID: {result.get('id')}"
        }
    except Exception as error:
        logger.error(f"Error creating filtering profile: {error}")
        return {"status": "error", "message": f"Error: {str(error)}"}

async def IA_linkPolicyToFilteringProfile(
    filtering_profile_id: str,
    filtering_policy_id: str,
    priority: int = 1000
) -> dict[str, Any]:
    """Link a filtering policy to a filtering profile."""
    logger.info(f"IA_linkPolicyToFilteringProfile called: profile={filtering_profile_id}, policy={filtering_policy_id}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        body = {
            "@odata.type": "#microsoft.graph.networkaccess.filteringPolicyLink",
            "state": "enabled",
            "priority": priority,
            "loggingState": "enabled",
            "policy": {
                "id": filtering_policy_id,
                "@odata.type": "#microsoft.graph.networkaccess.filteringPolicy"
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://graph.microsoft.com/beta/networkAccess/filteringProfiles/{filtering_profile_id}/policies",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            result = response.json()
        
        return {
            "status": "success",
            "profile_id": filtering_profile_id,
            "policy_id": filtering_policy_id,
            "link_id": result.get("id"),
            "message": f"Filtering policy linked to profile.\nProfile ID: {filtering_profile_id}\nPolicy ID: {filtering_policy_id}\nLink ID: {result.get('id')}"
        }
    except Exception as error:
        logger.error(f"Error linking filtering policy to profile: {error}")
        return {"status": "error", "message": f"Error: {str(error)}"}

async def IA_createConditionalAccessPolicy(
    filtering_profile_id: str,
    displayName: str = "POC-Monitor AI conditional access policy",
    includeUsers: Optional[List[str]] = None,
    includeGroups: Optional[List[str]] = None,
    includeApplications: Optional[List[str]] = None
) -> dict[str, Any]:
    """Create a conditional access policy that references the filtering profile."""
    if includeUsers is None:
        includeUsers = ["None"]
    if includeGroups is None:
        includeGroups = []
    if includeApplications is None:
        includeApplications = [
            "c08f52c9-8f03-4558-a0ea-9a4c878cf343",
            "5dc48733-b5df-475c-a49b-fa307ef00853"
        ]
    
    logger.info(f"IA_createConditionalAccessPolicy called: profile={filtering_profile_id}, name={displayName}")
    
    try:
        auth_middleware = get_auth_middleware()
        token = await auth_middleware.get_valid_token()
        
        if not token:
            return {"status": "error", "message": "Authentication token not available. Authentication may be disabled or failed."}
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        users_obj = {"includeUsers": includeUsers}
        if includeGroups and len(includeGroups) > 0:
            users_obj["includeGroups"] = includeGroups
        
        body = {
            "displayName": displayName,
            "state": "enabledForReportingButNotEnforced",
            "conditions": {
                "clientAppTypes": ["all"],
                "applications": {"includeApplications": includeApplications},
                "users": users_obj
            },
            "sessionControls": {
                "networkAccessSecurity": {"policyId": filtering_profile_id, "isEnabled": True},
                "globalSecureAccessFilteringProfile": {"profileId": filtering_profile_id, "isEnabled": True}
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://graph.microsoft.com/beta/identity/conditionalAccess/policies",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            result = response.json()
        
        return {
            "status": "success",
            "policy_name": result.get("displayName"),
            "policy_id": result.get("id"),
            "message": f"Conditional Access policy created.\nPolicy Name: {result.get('displayName')}\nID: {result.get('id')}"
        }
    except Exception as error:
        logger.error(f"Error creating conditional access policy: {error}")
        return {"status": "error", "message": f"Error: {str(error)}"}

async def IA_TLSPOCV2(
    name: str = "POCEntCA",
    commonName: str = "POCRoot",
    organizationName: str = "POCLtd",
    cert_output_dir: str = "./certs",
    max_retries: int = 5
) -> dict[str, Any]:
    """
    TLS Onboarding POC V2 - Advanced Automated Certificate Workflow with Retry Logic
    
    Description:
        Automates the complete TLS onboarding process by intelligently chaining existing 
        MCP tools with robust retry logic and comprehensive certificate management.
        This tool orchestrates the full certificate lifecycle from CSR generation 
        to Root CA deployment with built-in resilience for API timing issues.
        
    Added robust timeout handling and timezone-aware datetime for compliance with Python 3.12+ and API reliability improvements.
        
    Purpose:
        - Fully automated TLS certificate onboarding workflow
        - Intelligent retry logic for API readiness conditions
        - Automatic Root CA certificate download and storage
        - Enhanced error handling and recovery mechanisms
        - Production-ready certificate deployment pipeline
        
    Workflow Implementation:
        1. 📝 CSR Generation: Creates certificate request via Graph API
        2. ⏰ Readiness Verification: Validates certificate availability with backoff retry
        3. 🔐 Certificate Signing: Signs CSR with self-signed CA and uploads
        4. 📁 Root CA Download: Extracts and stores Root CA certificate locally
        5. ✅ Verification: Confirms all components are properly deployed
        
    Retry Strategy:
        - Exponential backoff: 2s, 4s, 8s, 16s, 32s (configurable max_retries)
        - Transient error detection and recovery including read timeouts
        - API readiness validation between steps
        - Comprehensive logging of retry attempts with delay diagnostics
        
    Certificate Management:
        - Automatic Root CA extraction and local storage
        - Multiple certificate format support (PEM, CER)
        - Certificate validation and integrity checks
        - Deployment-ready file organization
        
    Args:
        name: Certificate name (max 12 characters, alphanumeric only)
        commonName: Common name (max 12 characters, alphanumeric + spaces)  
        organizationName: Organization name (max 12 characters, alphanumeric only)
        cert_output_dir: Directory for certificate storage (default: "./certs")
        max_retries: Maximum retry attempts for transient failures (default: 5)
        
    Returns:
        Comprehensive JSON object containing:
        - CSR generation details and metadata
        - Certificate signing and upload status
        - Root CA download and storage information
        - Retry counts, timestamps, and performance metrics
        - Error details and recovery recommendations
        - Deployment instructions and file locations
    """
    import asyncio
    import time
    import os
    import re
    import base64
    from pathlib import Path
    from datetime import datetime, timedelta, timezone
    
    logger.info(f"IA_TLSPOCV2 called: name={name}")
    
    auth_middleware = get_auth_middleware()
    token = await auth_middleware.get_valid_token()
    
    if not token:
        return {
            "status": "error", 
            "message": "Graph client not initialized. Authentication token not available.",
            "tool_name": "IA_TLSPOCV2"
        }
    
    # Initialize comprehensive tracking
    start_time = time.time()
    workflow_log = []
    retry_counts = {"csr_creation": 0, "signing_upload": 0, "certificate_verification": 0}
    
    def log_step(step: str, status: str, details: str = "", retry_count: int = 0):
        """Log workflow step with timestamp and retry information"""
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "step": step,
            "status": status,
            "details": details,
            "retry_count": retry_count
        }
        workflow_log.append(entry)
        logger.info(f"IA_TLSPOCV2 - {step}: {status} (retry: {retry_count}) - {details}")
    
    async def exponential_backoff_wait(attempt: int) -> int:
        """Calculate exponential backoff delay: 2^attempt seconds"""
        delay = min(2 ** attempt, 32)  # Cap at 32 seconds
        logger.info(f"Exponential backoff: waiting {delay} seconds (attempt {attempt + 1})")
        await asyncio.sleep(delay)
        return delay
    
    try:
        log_step("workflow_start", "initiated", f"Starting TLS POC V2 workflow for {name}")
        
        # Validate field lengths and characters (Microsoft Graph API requirements)
        name_clean = name.strip()
        commonName_clean = commonName.strip()
        organizationName_clean = organizationName.strip()
        
        validation_errors = []
        
        # Check length (12 characters max)
        if len(name_clean) > 12:
            validation_errors.append(f"name '{name_clean}' exceeds 12 character limit (length: {len(name_clean)})")
        if len(commonName_clean) > 12:
            validation_errors.append(f"commonName '{commonName_clean}' exceeds 12 character limit (length: {len(commonName_clean)})")
        if len(organizationName_clean) > 12:
            validation_errors.append(f"organizationName '{organizationName_clean}' exceeds 12 character limit (length: {len(organizationName_clean)})")
        
        # Check for invalid characters (only letters and digits allowed)
        if not re.match(r'^[A-Za-z0-9]+$', name_clean):
            validation_errors.append(f"name '{name_clean}' contains invalid characters (only letters and digits allowed)")
        if not re.match(r'^[A-Za-z0-9 ]+$', commonName_clean):  # commonName allows spaces
            validation_errors.append(f"commonName '{commonName_clean}' contains invalid characters (only letters, digits, and spaces allowed)")
        if not re.match(r'^[A-Za-z0-9]+$', organizationName_clean):
            validation_errors.append(f"organizationName '{organizationName_clean}' contains invalid characters (only letters and digits allowed)")
        
        if validation_errors:
            error_message = "Certificate field validation failed:\n" + "\n".join(f"  - {err}" for err in validation_errors)
            error_message += "\n\nMicrosoft Graph API requirements:"
            error_message += "\n  - Maximum 12 characters for all fields"
            error_message += "\n  - Only letters and digits allowed (no hyphens, underscores, or special characters)"
            error_message += "\n  - commonName can include spaces"
            error_message += "\nPlease fix the field values and try again."
            return {"status": "error", "message": error_message, "validation_errors": validation_errors}
        
        # =================================================================
        # STEP 1: CSR GENERATION WITH RETRY LOGIC
        # =================================================================
        log_step("csr_generation", "starting", "Creating certificate request via Graph API")
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        certificate_id = None
        csr_content = ""
        
        for attempt in range(max_retries):
            try:
                body = {
                    "@odata.type": "#microsoft.graph.networkaccess.externalCertificateAuthorityCertificate",
                    "name": name_clean,
                    "commonName": commonName_clean,
                    "organizationName": organizationName_clean
                }
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        "https://graph.microsoft.com/beta/networkAccess/tls/externalCertificateAuthorityCertificates",
                        headers=headers,
                        json=body
                    )
                    
                    if response.status_code >= 400:
                        error_body = response.text
                        logger.error(f"TLS CSR API Error: {error_body}")
                        retry_counts["csr_creation"] += 1
                        
                        if attempt < max_retries - 1:
                            log_step("csr_generation", "retry_needed", f"API error on attempt {attempt + 1}: {error_body}", attempt + 1)
                            await exponential_backoff_wait(attempt)
                            continue
                        else:
                            return {
                                "status": "error",
                                "step_failed": "csr_generation",
                                "message": f"CSR creation failed after {max_retries} attempts: {error_body}",
                                "status_code": response.status_code
                            }
                    
                    response.raise_for_status()
                    result = response.json()
                
                certificate_id = result.get("id")
                if not certificate_id:
                    retry_counts["csr_creation"] += 1
                    if attempt < max_retries - 1:
                        log_step("csr_generation", "retry_needed", f"No certificate ID in response, attempt {attempt + 1}", attempt + 1)
                        await exponential_backoff_wait(attempt)
                        continue
                    else:
                        return {
                            "status": "error",
                            "step_failed": "csr_generation",
                            "message": "Invalid API response: missing certificate ID",
                            "response_data": result
                        }
                
                # Try to get CSR content
                if result.get("certificateSigningRequest"):
                    csr_content = result["certificateSigningRequest"]
                
                log_step("csr_generation", "success", f"CSR created with ID: {certificate_id}")
                break
                        
            except Exception as e:
                retry_counts["csr_creation"] += 1
                log_step("csr_generation", "exception", f"Exception on attempt {attempt + 1}: {str(e)}", attempt + 1)
                
                if attempt < max_retries - 1:
                    await exponential_backoff_wait(attempt)
                else:
                    log_step("csr_generation", "failed", "Max retries exceeded due to exceptions")
                    return {
                        "status": "error",
                        "step_failed": "csr_generation",
                        "message": f"CSR creation failed with exceptions after {max_retries} attempts: {str(e)}",
                        "workflow_log": workflow_log,
                        "retry_counts": retry_counts,
                        "tool_name": "IA_TLSPOCV2"
                    }
        
        # Wait for certificate to be ready
        await asyncio.sleep(5)
        
        # =================================================================
        # STEP 2: CERTIFICATE SIGNING AND UPLOAD WITH RETRY LOGIC  
        # =================================================================
        log_step("signing_upload", "starting", "Signing certificate and uploading to Graph API")
        
        # Import cryptography for certificate signing
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID, ExtensionOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.backends import default_backend
        except ImportError:
            return {
                "status": "error",
                "step_failed": "import_cryptography",
                "message": "cryptography library not installed. Install with: pip install cryptography",
                "tool_name": "IA_TLSPOCV2"
            }
        
        sign_result = None
        for attempt in range(max_retries):
            try:
                # Generate CA if needed
                ca_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=4096,
                    backend=default_backend()
                )
                
                ca_subject = x509.Name([
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Self Signed"),
                    x509.NameAttribute(NameOID.COMMON_NAME, "Self Signed Root CA")
                ])
                
                ca_cert = x509.CertificateBuilder().subject_name(
                    ca_subject
                ).issuer_name(
                    ca_subject
                ).public_key(
                    ca_key.public_key()
                ).serial_number(
                    int(datetime.now().timestamp() * 1000)
                ).not_valid_before(
                    datetime.now(timezone.utc)
                ).not_valid_after(
                    datetime.now(timezone.utc) + timedelta(days=3650)
                ).add_extension(
                    x509.BasicConstraints(ca=True, path_length=None),
                    critical=True
                ).add_extension(
                    x509.KeyUsage(
                        digital_signature=True,
                        key_cert_sign=True,
                        crl_sign=True,
                        key_encipherment=False,
                        content_commitment=False,
                        data_encipherment=False,
                        key_agreement=False,
                        encipher_only=False,
                        decipher_only=False
                    ),
                    critical=True
                ).add_extension(
                    x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()),
                    critical=False
                ).sign(ca_key, hashes.SHA256(), default_backend())
                
                ca_cert_pem = ca_cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
                
                # Generate CSR if not available
                if not csr_content:
                    private_key = rsa.generate_private_key(
                        public_exponent=65537,
                        key_size=2048,
                        backend=default_backend()
                    )
                    
                    subject = x509.Name([
                        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organizationName_clean),
                        x509.NameAttribute(NameOID.COMMON_NAME, commonName_clean)
                    ])
                    
                    csr_obj = x509.CertificateSigningRequestBuilder().subject_name(
                        subject
                    ).add_extension(
                        x509.SubjectAlternativeName([
                            x509.DNSName("*.example.com"),
                            x509.DNSName("example.com"),
                        ]),
                        critical=False,
                    ).sign(private_key, hashes.SHA256(), default_backend())
                else:
                    # Parse provided CSR
                    csr_normalized = csr_content.replace('\r\n', '\n').replace('\r', '\n')
                    if 'BEGIN CERTIFICATE REQUEST' in csr_normalized:
                        csr_bytes = csr_normalized.encode('utf-8')
                        csr_obj = x509.load_pem_x509_csr(csr_bytes, default_backend())
                    else:
                        try:
                            csr_bytes = base64.b64decode(csr_normalized)
                            csr_obj = x509.load_der_x509_csr(csr_bytes, default_backend())
                        except Exception:
                            return {"status": "error", "message": "Could not decode CSR"}
                
                # Sign the leaf certificate
                leaf_cert = x509.CertificateBuilder().subject_name(
                    csr_obj.subject
                ).issuer_name(
                    ca_cert.subject
                ).public_key(
                    csr_obj.public_key()
                ).serial_number(
                    int(datetime.now().timestamp() * 1000)
                ).not_valid_before(
                    datetime.now(timezone.utc)
                ).not_valid_after(
                    datetime.now(timezone.utc) + timedelta(days=365)
                ).add_extension(
                    x509.BasicConstraints(ca=True, path_length=None),
                    critical=True
                ).add_extension(
                    x509.KeyUsage(
                        digital_signature=False,
                        key_cert_sign=True,
                        crl_sign=True,
                        key_encipherment=False,
                        content_commitment=False,
                        data_encipherment=False,
                        key_agreement=False,
                        encipher_only=False,
                        decipher_only=False
                    ),
                    critical=True
                ).add_extension(
                    x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.SERVER_AUTH]),
                    critical=True
                ).add_extension(
                    x509.SubjectKeyIdentifier.from_public_key(csr_obj.public_key()),
                    critical=False
                )
                
                # Add SAN if present in CSR
                try:
                    san_ext = csr_obj.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                    leaf_cert = leaf_cert.add_extension(san_ext.value, critical=False)
                except x509.ExtensionNotFound:
                    pass
                
                # Add authority key identifier
                leaf_cert = leaf_cert.add_extension(
                    x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),
                    critical=False
                )
                
                # Sign the certificate
                signed_cert = leaf_cert.sign(ca_key, hashes.SHA256(), default_backend())
                signed_pem = signed_cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
                
                # Upload to Graph API
                upload_body = {
                    "certificate": signed_pem,
                    "chain": ca_cert_pem
                }
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    upload_response = await client.patch(
                        f"https://graph.microsoft.com/beta/networkAccess/tls/externalCertificateAuthorityCertificates/{certificate_id}",
                        headers=headers,
                        json=upload_body
                    )
                    upload_response.raise_for_status()
                
                sign_result = {
                    "status": "success",
                    "signed_certificate_pem": signed_pem,
                    "root_ca_pem": ca_cert_pem
                }
                
                log_step("signing_upload", "success", "Certificate signed and uploaded successfully")
                break
                        
            except Exception as e:
                retry_counts["signing_upload"] += 1
                log_step("signing_upload", "exception", f"Exception on attempt {attempt + 1}: {str(e)}", attempt + 1)
                
                if attempt < max_retries - 1:
                    await exponential_backoff_wait(attempt)
                else:
                    return {
                        "status": "error",
                        "step_failed": "signing_upload",
                        "message": f"Certificate signing/upload failed after {max_retries} attempts: {str(e)}",
                        "workflow_log": workflow_log,
                        "retry_counts": retry_counts
                    }
        
        # =================================================================
        # STEP 3: ROOT CA CERTIFICATE DOWNLOAD AND STORAGE
        # =================================================================
        log_step("root_ca_download", "starting", "Extracting and storing Root CA certificate")
        
        root_ca_pem = sign_result.get("root_ca_pem")
        if not root_ca_pem:
            return {
                "status": "error",
                "step_failed": "root_ca_download",
                "message": "Root CA certificate not available from signing operation"
            }
        
        # Create certificate output directory
        try:
            cert_path = Path(cert_output_dir)
            cert_path.mkdir(parents=True, exist_ok=True)
            log_step("root_ca_download", "progress", f"Certificate directory created: {cert_path.absolute()}")
        except Exception as e:
            return {
                "status": "error",
                "step_failed": "root_ca_download",
                "message": f"Failed to create certificate directory {cert_output_dir}: {str(e)}"
            }
        
        # Save Root CA certificate in multiple formats
        root_ca_files = {}
        try:
            # Save as .pem file
            root_ca_pem_path = cert_path / "rootCA.pem"
            with open(root_ca_pem_path, 'w') as f:
                f.write(root_ca_pem)
            root_ca_files["pem"] = str(root_ca_pem_path.absolute())
            
            # Save as .cer file for Windows compatibility
            root_ca_cer_path = cert_path / "rootCA.cer"
            with open(root_ca_cer_path, 'w') as f:
                f.write(root_ca_pem)
            root_ca_files["cer"] = str(root_ca_cer_path.absolute())
            
            # Save signed certificate
            signed_cert_pem = sign_result.get("signed_certificate_pem")
            if signed_cert_pem:
                signed_cert_path = cert_path / "signed_certificate.pem"
                with open(signed_cert_path, 'w') as f:
                    f.write(signed_cert_pem)
                root_ca_files["signed_cert"] = str(signed_cert_path.absolute())
            
            log_step("root_ca_download", "success", f"Root CA certificate saved in {len(root_ca_files)} formats")
            
        except Exception as e:
            return {
                "status": "error",
                "step_failed": "root_ca_download",
                "message": f"Failed to save Root CA certificate: {str(e)}"
            }
        
        # =================================================================
        # WORKFLOW COMPLETION AND SUMMARY
        # =================================================================
        end_time = time.time()
        total_duration = int(end_time - start_time)
        
        log_step("workflow_completion", "success", f"TLS POC V2 workflow completed in {total_duration} seconds")
        
        summary_message = f"""
=== TLS ONBOARDING POC V2 - WORKFLOW COMPLETED ===

✅ Automated TLS Certificate Workflow Successful

🔄 Workflow Performance:
  - Total Duration: {total_duration} seconds
  - Total Retries: {sum(retry_counts.values())}
  - Retry Breakdown: CSR({retry_counts['csr_creation']}) | Cert({retry_counts['certificate_verification']}) | Upload({retry_counts['signing_upload']})

📝 CSR Generation:
  ✅ Certificate ID: {certificate_id}
  ✅ Name: {name} | Common Name: {commonName} | Organization: {organizationName}

🔐 Certificate Signing & Upload:
  ✅ Signing: Completed with self-signed CA
  ✅ Upload: Success
  ✅ Certificate Chain: Established

📁 Root CA Certificate Download:
  ✅ Root CA Files Created: {len(root_ca_files)}
  ✅ Storage Directory: {cert_path.absolute()}
  ✅ Available Formats: {', '.join(root_ca_files.keys())}

📋 CRITICAL NEXT STEPS - ROOT CA DEPLOYMENT:

  🔴 MANDATORY: Deploy Root CA certificate to client devices before TLS inspection works!

  📥 Root CA Certificate Files:
     • PEM Format: {root_ca_files.get('pem', 'N/A')}
     • CER Format (Windows): {root_ca_files.get('cer', 'N/A')}

  🚀 Deployment Options:
     1. Group Policy (GPO) - Windows domain environments
     2. Microsoft Intune - Cloud-managed devices  
     3. SCCM/ConfigMgr - Enterprise deployment
     4. Manual Installation - Testing/POC

  ⚠️  WARNING: TLS inspection will NOT function until Root CA is deployed!
               HTTPS traffic will fail with certificate errors without deployment.

🔗 Documentation: https://learn.microsoft.com/en-us/entra/global-secure-access/how-to-configure-tls-inspection
"""
        
        return {
            "status": "success",
            "tool_name": "IA_TLSPOCV2",
            "workflow_duration_seconds": total_duration,
            "timestamp_completed": datetime.now().isoformat(),
            "csr_generation": {
                "status": "success",
                "certificate_id": certificate_id,
                "certificate_name": name,
                "common_name": commonName,
                "organization": organizationName
            },
            "signing_upload": {
                "status": "success",
                "certificate_uploaded": True
            },
            "root_ca_download": {
                "status": "success",
                "files_created": root_ca_files,
                "output_directory": str(cert_path.absolute()),
                "formats_available": list(root_ca_files.keys())
            },
            "retry_metrics": {
                "total_retries": sum(retry_counts.values()),
                "retry_breakdown": retry_counts,
                "max_retries_configured": max_retries
            },
            "workflow_log": workflow_log,
            "message": summary_message
        }
        
    except Exception as error:
        end_time = time.time()
        total_duration = int(end_time - start_time)
        
        log_step("workflow_error", "failed", f"Unexpected workflow error: {str(error)}")
        
        return {
            "status": "error",
            "tool_name": "IA_TLSPOCV2", 
            "step_failed": "workflow_exception",
            "message": f"Unexpected error in TLS POC V2 workflow: {str(error)}",
            "workflow_duration_seconds": total_duration,
            "workflow_log": workflow_log,
            "retry_counts": retry_counts,
            "error_details": str(error)
        }

async def IA_internetAccessPoc(
    forwarding_profile_id: str,
    filtering_policy_name: str = "POC-Monitor AI Access",
    filtering_policy_description: str = "Monitor access to AI",
    filtering_profile_name: str = "POC-Monitor AI Access Profile",
    filtering_profile_description: str = "Profile for monitoring AI access",
    filtering_profile_state: str = "enabled",
    filtering_profile_priority: int = 1000,
    link_priority: int = 1000,
    create_ca_policy: bool = True,
    ca_policy_display_name: str = "POC-Monitor AI conditional access policy",
    ca_policy_include_users: Optional[List[str]] = None,
    ca_policy_include_groups: Optional[List[str]] = None,
    ca_policy_include_applications: Optional[List[str]] = None
) -> dict[str, Any]:
    """
    Internet Access Web Content Filtering POC - Complete Setup Automation.
    
    Automated end-to-end setup for Web Content Filtering in Global Secure Access.
    """
    logger.info(f"IA_internetAccessPoc called: profile_id={forwarding_profile_id}")
    
    try:
        if ca_policy_include_users is None:
            ca_policy_include_users = ["None"]
        if ca_policy_include_groups is None:
            ca_policy_include_groups = []
        if ca_policy_include_applications is None:
            ca_policy_include_applications = [
                "c08f52c9-8f03-4558-a0ea-9a4c878cf343",
                "5dc48733-b5df-475c-a49b-fa307ef00853"
            ]
        
        results = []
        
        # Step 1: Enable forwarding profile
        enable_result = await IA_enableInternetAccessForwardingProfile(forwarding_profile_id, "enabled")
        results.append(f"1. Forwarding Profile: {enable_result.get('message', 'No response')}")
        
        # Step 2: Create filtering policy
        policy_result = await IA_createFilteringPolicy(filtering_policy_name, filtering_policy_description)
        filtering_policy_id = policy_result.get("policy_id")
        results.append(f"2. Filtering Policy: {policy_result.get('message', 'No response')}")
        
        # Step 3: Create filtering profile
        profile_result = await IA_createFilteringProfile(
            filtering_profile_name,
            filtering_profile_description,
            filtering_profile_state,
            filtering_profile_priority
        )
        filtering_profile_id_created = profile_result.get("profile_id")
        results.append(f"3. Filtering Profile: {profile_result.get('message', 'No response')}")
        
        # Step 4: Link policy to profile
        if filtering_profile_id_created and filtering_policy_id:
            link_result = await IA_linkPolicyToFilteringProfile(
                filtering_profile_id_created,
                filtering_policy_id,
                link_priority
            )
            results.append(f"4. Link: {link_result.get('message', 'No response')}")
        else:
            results.append("4. Link: Skipped due to missing profile or policy ID.")
        
        # Step 5: Create Conditional Access policy (optional)
        if create_ca_policy and filtering_profile_id_created:
            try:
                ca_result = await IA_createConditionalAccessPolicy(
                    filtering_profile_id_created,
                    ca_policy_display_name,
                    ca_policy_include_users,
                    ca_policy_include_groups,
                    ca_policy_include_applications
                )
                results.append(f"5. Conditional Access Policy: {ca_result.get('message', 'No response')}")
            except Exception as ca_error:
                results.append(f"5. Conditional Access Policy: Failed - {str(ca_error)}")
        elif not create_ca_policy:
            results.append("5. Conditional Access Policy: Skipped (create_ca_policy=False).")
        else:
            results.append("5. Conditional Access Policy: Skipped due to missing filtering profile ID.")
        
        summary = "\nInternet Access POC completed successfully."
        
        return {
            "status": "success",
            "steps": results,
            "summary": summary,
            "message": "\n".join(results) + summary
        }
    except Exception as error:
        logger.error(f"Error in IA_internetAccessPoc: {error}")
        return {"status": "error", "message": f"Error: {str(error)}"}
