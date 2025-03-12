import sys
import os
from claude_tools.weather import register_weather_tools
from claude_tools.calculator import register_calculator_tools
from claude_tools.datetime_tool import register_datetime_tools
from mcp.server.fastmcp import FastMCP

def main():
    """
    Main entry point for the claude-tools package.
    This function initializes and runs the MCP server with the registered tools.
    """
    print("Starting Claude Tools MCP server...", file=sys.stderr)
    
    # Initialize FastMCP server
    mcp = FastMCP("claude-tools")
    
    # Register all tools
    print("Registering weather tools...", file=sys.stderr)
    register_weather_tools(mcp)
    
    print("Registering calculator tools...", file=sys.stderr)
    register_calculator_tools(mcp)
    
    print("Registering datetime tools...", file=sys.stderr)
    register_datetime_tools(mcp)
    
    print("Starting server with stdio transport...", file=sys.stderr)
    try:
        # Run the server with stdio transport
        mcp.run(transport='stdio')
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()