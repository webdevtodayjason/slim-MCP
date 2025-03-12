from datetime import datetime, timezone

def get_current_time() -> str:
    """Get the current date and time.
    """
    now = datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

def get_current_utc_time() -> str:
    """Get the current UTC date and time.
    """
    now = datetime.now(timezone.utc)
    return f"Current UTC date and time: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}"

def register_datetime_tools(mcp):
    """Register all datetime tools with the MCP server."""
    mcp.tool()(get_current_time)
    mcp.tool()(get_current_utc_time)
