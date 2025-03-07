# Slim MCP (Multi-purpose Control Program)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A lightweight, modular API service that provides a collection of useful tools through a consistent RESTful interface. Perfect for integrating with AI agents, automated workflows, or as a backend for utility applications.

![MCP System](https://raw.githubusercontent.com/webdevtodayjason/slim-MCP/main/mcp_header.png)

## 🚀 Features

- **🌤️ Weather**: Get current weather for any location
- **📅 Date & Time**: Format and manipulate dates
- **📆 Calendar**: Generate monthly calendars and upcoming dates
- **✅ Tasks**: Simple task management system
- **📧 Email**: Send emails via Mailgun
- **💰 Currency**: Convert between currencies and get exchange rates
- **🧮 Calculator**: Perform basic arithmetic calculations
- **🔍 Search**: Simple web search functionality
- **🖥️ Cursor Integration**: Supports [Cursor](https://cursor.sh) Model Context Protocol

## 📋 Requirements

- Python 3.6+
- Flask
- Requests
- BeautifulSoup4
- python-dotenv

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/webdevtodayjason/slim-MCP.git
cd slim-MCP

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## 🚀 Usage

### Starting the Server

```bash
python mcp_server.py
```

This will start the server on port 5734 by default. You can change the port by setting the `PORT` environment variable in your `.env` file.

### API Endpoints

All tools are accessible through RESTful endpoints:

```
GET  /tools                      # List all available tools
POST /tools/weather              # Get weather for a location
POST /tools/datetime             # Get current date and time
POST /tools/datetime_format      # Format a date string
POST /tools/calculator           # Perform calculations
POST /tools/duckduckgo_search    # Search the web
POST /tools/email                # Send an email
POST /tools/calendar             # Get a month calendar
POST /tools/upcoming_dates       # Get upcoming dates
POST /tools/tasks_add            # Add a new task
POST /tools/tasks_get            # Get tasks
POST /tools/tasks_update         # Update a task
POST /tools/tasks_delete         # Delete a task
POST /tools/currency_convert     # Convert between currencies
POST /tools/currency_rates       # Get exchange rates
```

## 🔍 Examples

### Get Current Weather

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"location": "Tokyo"}' \
  http://localhost:5734/tools/weather
```

### Format a Date

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"date_str": "2025-03-05", "format_str": "%A, %B %d, %Y"}' \
  http://localhost:5734/tools/datetime_format
```

### Get a Monthly Calendar

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"year": 2025, "month": 3}' \
  http://localhost:5734/tools/calendar
```

### Send an Email

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"to": "recipient@example.com", "subject": "Hello from MCP", "text": "This is a test email from the Multi-purpose Control Program", "from_name": "MCP"}' \
  http://localhost:5734/tools/email
```

### Add a Task

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"title": "Complete project", "description": "Finish the MCP project", "due_date": "2025-03-15", "priority": "high"}' \
  http://localhost:5734/tools/tasks_add
```

## 🔧 Extending

Adding new tools is easy:

1. Create a new Python module file (e.g., `new_tool.py`)
2. Define your tool functions in that file
3. Register the tool in the `tools` dictionary in `mcp_server.py`
4. Add route handlers that call your tool functions

## 🖥️ Cursor Integration

This server implements the [Cursor Model Context Protocol](https://docs.cursor.com/context/model-context-protocol), allowing it to be used as a context provider for Cursor, the AI-native code editor.

### Setting up with Cursor:

1. Start either:
   - Full MCP server: `python mcp_server.py`, OR
   - Simple Cursor server: `python simple_cursor_server.py` (if you're having connection issues)
   
2. In Cursor, go to Settings > Chat > Context Providers
3. Add a new context provider with the following URL:
   ```
   http://localhost:5734/cursor/context
   ```
4. Content type: Select "sse" from the dropdown
5. Test the connection by clicking "Test Connection"
6. Start using Cursor with MCP as your context provider!

The Cursor integration provides:
- Web search capabilities (`/cursor/context/search`)
- Content retrieval (`/cursor/context/retrieve`)
- Health check endpoint (`/cursor/health`)

If you encounter connection issues with the full MCP server, try using the simple Cursor server instead, which is specifically designed for Cursor integration.

## 📝 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Jason Brashear** - [webdevtodayjason](https://github.com/webdevtodayjason)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/webdevtodayjason">Jason Brashear</a>
</p>