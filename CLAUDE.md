# MCP (Multi-purpose Control Program) Codebase Guidelines

## Run Commands
- Start server: `python mcp_server.py`
- Install dependencies: `pip install -r requirements.txt`
- Set up environment: Copy `.env.example` to `.env` and add your API keys
- Test endpoint: `curl -X POST -H "Content-Type: application/json" http://localhost:5734/tools/datetime`

## Code Style Guidelines
- **Imports**: Standard library first, then third-party packages, then local modules
- **Naming**: Use snake_case for variables, functions, and endpoints
- **Typing**: Consider adding type hints for better code clarity
- **Error Handling**: Use try/except with specific error types and detailed error messages
- **API Structure**: RESTful endpoints with consistent JSON response format
- **Documentation**: Add docstrings for functions and meaningful comments
- **Environment Variables**: Use python-dotenv for configuration and secrets
- **Response Format**: Always return JSON with either `result` or `error` keys
- **HTTP Status Codes**: Use appropriate status codes (200, 400, 500) for responses

## Project Structure
The codebase follows a modular tool-based architecture exposing various utility APIs through Flask endpoints:
- Each tool has its own module file (e.g., `calendar_tool.py`, `email_tool.py`)
- The main server file (`mcp_server.py`) registers and exposes these tools
- Tools are registered in the `tools` dictionary with descriptions and parameters

## Available Tools
- Weather: Get current weather for a location
- DateTime: Get current date and time information
- Calendar: Get monthly calendars and upcoming dates
- Tasks: Simple task management (add, get, update, delete)
- Email: Send emails via Mailgun
- Currency: Currency conversion and exchange rates