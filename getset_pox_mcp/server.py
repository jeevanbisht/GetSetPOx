"""
Main MCP server implementation for getset-pox-mcp.

This module provides the core MCP server with tool registration and
transport layer handling (STDIO and HTTP).
"""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from getset_pox_mcp.config import ServerConfig
from getset_pox_mcp.logging_config import setup_logging, get_logger
from getset_pox_mcp.services import (
    hello_world, echo, check_token_permissions,
    IA_checkInternetAccessForwardingProfile,
    IA_enableInternetAccessForwardingProfile,
    IA_createFilteringPolicy,
    IA_createFilteringProfile,
    IA_linkPolicyToFilteringProfile,
    IA_createConditionalAccessPolicy,
    IA_TLSPOCV2,
    IA_internetAccessPoc,
    GovernInternetAccessPOC,
    IGA_listAccessPackages,
    IGA_createAccessCatalog,
    IGA_createAccessPackage,
    IGA_addResourceGrouptoPackage,
    IN_listIntuneManagedDevices,
    IN_getManagedDeviceDetails,
    IN_listDeviceCompliancePolicies,
    IN_listDeviceConfigurationProfiles,
    IN_syncManagedDevice,
    IN_prepGSAWinClient,
    IN_intuneAppAssignment,
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
from getset_pox_mcp.services.Test.hello_world_tools import get_hello_world_tool
from getset_pox_mcp.services.Test.echo_tools import get_echo_tool
from getset_pox_mcp.services.diagnostics.diagnostics_tools import get_check_token_permissions_tool
from getset_pox_mcp.services.internetAccess.internetAccess_tools import (
    get_IA_checkInternetAccessForwardingProfile_tool,
    get_IA_enableInternetAccessForwardingProfile_tool,
    get_IA_createFilteringPolicy_tool,
    get_IA_createFilteringProfile_tool,
    get_IA_linkPolicyToFilteringProfile_tool,
    get_IA_createConditionalAccessPolicy_tool,
    get_IA_TLSPOCV2_tool,
    get_IA_internetAccessPoc_tool,
)
from getset_pox_mcp.services.poc.poc_tools import get_GovernInternetAccessPOC_tool
from getset_pox_mcp.services.iga.iga_tools import (
    get_IGA_listAccessPackages_tool,
    get_IGA_createAccessCatalog_tool,
    get_IGA_createAccessPackage_tool,
    get_IGA_addResourceGrouptoPackage_tool,
)
from getset_pox_mcp.services.intune.intune_tools import (
    get_IN_listIntuneManagedDevices_tool,
    get_IN_getManagedDeviceDetails_tool,
    get_IN_listDeviceCompliancePolicies_tool,
    get_IN_listDeviceConfigurationProfiles_tool,
    get_IN_syncManagedDevice_tool,
    get_IN_prepGSAWinClient_tool,
    get_IN_intuneAppAssignment_tool,
)
from getset_pox_mcp.services.eid.eid_tools import (
    get_EID_listUsers_tool,
    get_EID_getUser_tool,
    get_EID_searchUsers_tool,
    get_EID_listDevices_tool,
    get_EID_getDevice_tool,
    get_EID_getGroups_tool,
    get_EID_getGroup_tool,
    get_EID_getGroupMembers_tool,
    get_EID_searchGroups_tool,
    get_EID_createUserGroups_tool,
)
from getset_pox_mcp.authentication.middleware import get_auth_middleware

# Initialize server
mcp = Server("getset-pox-mcp")
logger = get_logger(__name__)


def register_tools() -> None:
    """Register all MCP tools with the server."""
    
    @mcp.list_tools()
    async def list_tools() -> list[Tool]:
        """
        List all available tools.
        
        Returns:
            List of Tool objects describing available tools.
        """
        return [
            get_hello_world_tool(),
            get_echo_tool(),
            get_check_token_permissions_tool(),
            get_IA_checkInternetAccessForwardingProfile_tool(),
            get_IA_enableInternetAccessForwardingProfile_tool(),
            get_IA_createFilteringPolicy_tool(),
            get_IA_createFilteringProfile_tool(),
            get_IA_linkPolicyToFilteringProfile_tool(),
            get_IA_createConditionalAccessPolicy_tool(),
            get_IA_TLSPOCV2_tool(),
            get_IA_internetAccessPoc_tool(),
            get_GovernInternetAccessPOC_tool(),
            get_IGA_listAccessPackages_tool(),
            get_IGA_createAccessCatalog_tool(),
            get_IGA_createAccessPackage_tool(),
            get_IGA_addResourceGrouptoPackage_tool(),
            get_IN_listIntuneManagedDevices_tool(),
            get_IN_getManagedDeviceDetails_tool(),
            get_IN_listDeviceCompliancePolicies_tool(),
            get_IN_listDeviceConfigurationProfiles_tool(),
            get_IN_syncManagedDevice_tool(),
            get_IN_prepGSAWinClient_tool(),
            get_IN_intuneAppAssignment_tool(),
            get_EID_listUsers_tool(),
            get_EID_getUser_tool(),
            get_EID_searchUsers_tool(),
            get_EID_listDevices_tool(),
            get_EID_getDevice_tool(),
            get_EID_getGroups_tool(),
            get_EID_getGroup_tool(),
            get_EID_getGroupMembers_tool(),
            get_EID_searchGroups_tool(),
            get_EID_createUserGroups_tool(),
        ]
    
    @mcp.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """
        Handle tool invocation.
        
        Args:
            name: Name of the tool to invoke
            arguments: Dictionary of tool arguments
        
        Returns:
            List of TextContent objects containing the tool result.
        
        Raises:
            ValueError: If the tool name is unknown.
        """
        logger.info(f"Tool called: {name} with arguments: {arguments}")
        
        try:
            if name == "hello_world":
                result = await hello_world(**arguments)
            elif name == "echo":
                result = await echo(**arguments)
            elif name == "check_token_permissions":
                result = await check_token_permissions(**arguments)
            elif name == "IA_checkInternetAccessForwardingProfile":
                result = await IA_checkInternetAccessForwardingProfile(**arguments)
            elif name == "IA_enableInternetAccessForwardingProfile":
                result = await IA_enableInternetAccessForwardingProfile(**arguments)
            elif name == "IA_createFilteringPolicy":
                result = await IA_createFilteringPolicy(**arguments)
            elif name == "IA_createFilteringProfile":
                result = await IA_createFilteringProfile(**arguments)
            elif name == "IA_linkPolicyToFilteringProfile":
                result = await IA_linkPolicyToFilteringProfile(**arguments)
            elif name == "IA_createConditionalAccessPolicy":
                result = await IA_createConditionalAccessPolicy(**arguments)
            elif name == "IA_TLSPOCV2":
                result = await IA_TLSPOCV2(**arguments)
            elif name == "IA_internetAccessPoc":
                result = await IA_internetAccessPoc(**arguments)
            elif name == "GovernInternetAccessPOC":
                result = await GovernInternetAccessPOC(**arguments)
            elif name == "IGA_listAccessPackages":
                result = await IGA_listAccessPackages(**arguments)
            elif name == "IGA_createAccessCatalog":
                result = await IGA_createAccessCatalog(**arguments)
            elif name == "IGA_createAccessPackage":
                result = await IGA_createAccessPackage(**arguments)
            elif name == "IGA_addResourceGrouptoPackage":
                result = await IGA_addResourceGrouptoPackage(**arguments)
            elif name == "IN_listIntuneManagedDevices":
                result = await IN_listIntuneManagedDevices(**arguments)
            elif name == "IN_getManagedDeviceDetails":
                result = await IN_getManagedDeviceDetails(**arguments)
            elif name == "IN_listDeviceCompliancePolicies":
                result = await IN_listDeviceCompliancePolicies(**arguments)
            elif name == "IN_listDeviceConfigurationProfiles":
                result = await IN_listDeviceConfigurationProfiles(**arguments)
            elif name == "IN_syncManagedDevice":
                result = await IN_syncManagedDevice(**arguments)
            elif name == "IN_prepGSAWinClient":
                result = await IN_prepGSAWinClient(**arguments)
            elif name == "IN_intuneAppAssignment":
                result = await IN_intuneAppAssignment(**arguments)
            elif name == "EID_listUsers":
                result = await EID_listUsers(**arguments)
            elif name == "EID_getUser":
                result = await EID_getUser(**arguments)
            elif name == "EID_searchUsers":
                result = await EID_searchUsers(**arguments)
            elif name == "EID_listDevices":
                result = await EID_listDevices(**arguments)
            elif name == "EID_getDevice":
                result = await EID_getDevice(**arguments)
            elif name == "EID_getGroups":
                result = await EID_getGroups(**arguments)
            elif name == "EID_getGroup":
                result = await EID_getGroup(**arguments)
            elif name == "EID_getGroupMembers":
                result = await EID_getGroupMembers(**arguments)
            elif name == "EID_searchGroups":
                result = await EID_searchGroups(**arguments)
            elif name == "EID_createUserGroups":
                result = await EID_createUserGroups(**arguments)
            else:
                error_msg = f"Unknown tool: {name}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            logger.debug(f"Tool {name} returned: {result}")
            
            # Format result as JSON string
            import json
            result_text = json.dumps(result, indent=2)
            
            return [TextContent(type="text", text=result_text)]
            
        except Exception as e:
            logger.exception(f"Error executing tool {name}: {e}")
            error_response = {
                "error": str(e),
                "tool": name,
                "arguments": arguments,
            }
            import json
            return [TextContent(type="text", text=json.dumps(error_response, indent=2))]


async def run_stdio() -> None:
    """Run the server with STDIO transport."""
    logger.info("Starting MCP server with STDIO transport")
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("STDIO transport initialized")
        await mcp.run(
            read_stream,
            write_stream,
            mcp.create_initialization_options(),
        )


async def run_http(config: ServerConfig) -> None:
    """
    Run the server with HTTP transport.
    
    Args:
        config: Server configuration containing HTTP settings.
    """
    logger.info(
        f"Starting MCP server with HTTP transport on "
        f"{config.http_host}:{config.http_port}{config.http_path}"
    )
    
    try:
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route
        import uvicorn
        
        sse = SseServerTransport(config.http_path)
        
        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await mcp.run(
                    streams[0], streams[1], mcp.create_initialization_options()
                )
        
        async def handle_messages(request):
            await sse.handle_post_message(request.scope, request.receive, request._send)
        
        app = Starlette(
            routes=[
                Route(config.http_path, endpoint=handle_sse),
                Route(config.http_path + "/messages", endpoint=handle_messages, methods=["POST"]),
            ]
        )
        
        logger.info("HTTP transport initialized")
        
        uvicorn_config = uvicorn.Config(
            app,
            host=config.http_host,
            port=config.http_port,
            log_level=config.log_level.lower(),
        )
        server = uvicorn.Server(uvicorn_config)
        await server.serve()
        
    except ImportError as e:
        logger.error(f"HTTP transport dependencies not installed: {e}")
        logger.error("Install with: pip install 'getset-pox-mcp[http]'")
        raise


async def async_main() -> None:
    """Main async entry point."""
    # Load configuration
    config = ServerConfig.from_env()
    config.validate()
    
    # Setup logging
    setup_logging(log_level=config.log_level, log_file=config.log_file)
    logger.info("getset-pox-mcp server starting")
    logger.info(f"Configuration: transport={config.transport}, log_level={config.log_level}")
    
    # Initialize authentication middleware
    auth_middleware = get_auth_middleware()
    auth_status = auth_middleware.get_auth_status()
    logger.info(f"Authentication: enabled={auth_status['enabled']}, mode={auth_status.get('mode', 'N/A')}")
    
    # Authenticate server in background if auth is enabled
    # This prevents blocking the MCP server initialization
    if auth_status['enabled']:
        logger.info("Server authentication will occur in background")
        asyncio.create_task(auth_middleware.authenticate_server())
    
    # Register tools
    register_tools()
    logger.info("Tools registered successfully")
    
    # Run appropriate transport
    if config.transport == "stdio":
        await run_stdio()
    elif config.transport == "http":
        await run_http(config)
    else:
        raise ValueError(f"Unsupported transport: {config.transport}")


def main() -> None:
    """Main entry point for the server."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.exception(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
