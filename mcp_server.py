from flask import Flask, jsonify, request, Response, make_response
import datetime
import requests
import os
import json
import traceback
from bs4 import BeautifulSoup
from dotenv import load_dotenv  # Import python-dotenv
from functools import wraps

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# CORS support for Cursor integration
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
    
# Handle OPTIONS requests for CORS preflight
@app.route('/', methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path=""):
    return make_response("", 200)

# MCP Tools Registry
tools = {
    "weather": {
        "description": "Get current weather for a location",
        "parameters": {"location": {"type": "string", "description": "City name (e.g., Tokyo)"}}
    },
    "datetime": {
        "description": "Get current date, time, and day of week",
        "parameters": {}
    },
    "datetime_format": {
        "description": "Format a date string according to specified format",
        "parameters": {
            "date_str": {"type": "string", "description": "Date string (ISO format or YYYY-MM-DD)"},
            "format_str": {"type": "string", "description": "Format string (e.g., %Y-%m-%d %H:%M:%S)"}
        }
    },
    "calculator": {
        "description": "Perform basic arithmetic calculations",
        "parameters": {"expression": {"type": "string", "description": "Math expression (e.g., 5 + 3)"}}
    },
    "duckduckgo_search": {
        "description": "Search the web using DuckDuckGo",
        "parameters": {"query": {"type": "string", "description": "Search term"}}
    },
    "email": {
        "description": "Send an email using Mailgun",
        "parameters": {
            "to": {"type": "string", "description": "Recipient email address"},
            "subject": {"type": "string", "description": "Email subject"},
            "text": {"type": "string", "description": "Email body content"},
            "from_name": {"type": "string", "description": "Sender name (optional)"}
        }
    },
    "calendar": {
        "description": "Get calendar for a specific month",
        "parameters": {
            "year": {"type": "integer", "description": "Year (optional, defaults to current)"},
            "month": {"type": "integer", "description": "Month 1-12 (optional, defaults to current)"}
        }
    },
    "upcoming_dates": {
        "description": "Get upcoming dates of a specific type",
        "parameters": {
            "date_type": {"type": "string", "description": "Type of dates (weekend, business_days)"},
            "count": {"type": "integer", "description": "Number of dates to retrieve (optional)"}
        }
    },
    "tasks_add": {
        "description": "Add a new task",
        "parameters": {
            "title": {"type": "string", "description": "Task title"},
            "description": {"type": "string", "description": "Task description (optional)"},
            "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format (optional)"},
            "priority": {"type": "string", "description": "Priority: low, medium, high (optional)"}
        }
    },
    "tasks_get": {
        "description": "Get tasks with optional filtering",
        "parameters": {
            "filter_type": {"type": "string", "description": "Filter: all, active, completed (optional)"}
        }
    },
    "tasks_update": {
        "description": "Update a task",
        "parameters": {
            "task_id": {"type": "integer", "description": "Task ID to update"},
            "updates": {"type": "object", "description": "Fields to update"}
        }
    },
    "tasks_delete": {
        "description": "Delete a task",
        "parameters": {
            "task_id": {"type": "integer", "description": "Task ID to delete"}
        }
    },
    "currency_convert": {
        "description": "Convert between currencies",
        "parameters": {
            "from_currency": {"type": "string", "description": "Source currency code (e.g., USD)"},
            "to_currency": {"type": "string", "description": "Target currency code (e.g., EUR)"},
            "amount": {"type": "number", "description": "Amount to convert"}
        }
    },
    "currency_rates": {
        "description": "Get exchange rates for a base currency",
        "parameters": {
            "base_currency": {"type": "string", "description": "Base currency code (e.g., USD)"}
        }
    }
}

@app.route('/tools', methods=['GET'])
def get_tools():
    return jsonify({"tools": tools})

@app.route('/tools/weather', methods=['POST'])
def weather_tool():
    data = request.get_json()
    location = data.get("location", "New York")
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")  # Load from .env
    if not api_key:
        return jsonify({"error": "OpenWeatherMap API key not configured"}), 500
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response_raw = requests.get(url)
        response = response_raw.json()
        print(f"Weather API response: {response}")  # Debug print
        if response.get("cod") == 200:
            result = {"temp": response["main"]["temp"], "desc": response["weather"][0]["description"]}
            return jsonify({"result": result})
        return jsonify({"error": f"Weather fetch failed: {response}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tools/datetime', methods=['POST'])
def datetime_tool():
    now = datetime.datetime.now()
    result = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A")
    }
    return jsonify({"result": result})

@app.route('/tools/calculator', methods=['POST'])
def calculator_tool():
    data = request.get_json()
    expr = data.get("expression", "0")
    try:
        result = eval(expr, {"__builtins__": {}})
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": "Invalid expression"}), 400

@app.route('/tools/duckduckgo_search', methods=['POST'])
def duckduckgo_search_tool():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Query is required"}), 400
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for result in soup.find_all("div", class_="result__body", limit=3):
            title = result.find("a", class_="result__a").text if result.find("a", class_="result__a") else "No title"
            snippet = result.find("div", class_="result__snippet").text if result.find("div", class_="result__snippet") else "No snippet"
            results.append({"title": title, "snippet": snippet})
        return jsonify({"result": results if results else "No results found"})
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

# Import all tool modules
from date_time_tool import get_current_datetime, format_date
from calendar_tool import get_month_calendar, get_upcoming_dates
from email_tool import send_email
from task_tool import add_task, get_tasks, update_task, delete_task
from currency_tool import convert_currency, get_exchange_rates
from cursor_context import CursorContextProvider

# Initialize the Cursor Context Provider
cursor_provider = CursorContextProvider()

@app.route('/tools/datetime_format', methods=['POST'])
def datetime_format_tool():
    data = request.get_json()
    date_str = data.get("date_str")
    format_str = data.get("format_str")
    
    if not date_str or not format_str:
        return jsonify({"error": "Both date_str and format_str are required"}), 400
    
    result = format_date(date_str, format_str)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

@app.route('/tools/email', methods=['POST'])
def email_tool():
    data = request.get_json()
    to = data.get("to")
    subject = data.get("subject")
    text = data.get("text")
    from_name = data.get("from_name")
    
    if not to or not subject or not text:
        return jsonify({"error": "Email recipient, subject, and body are required"}), 400
    
    result = send_email(to, subject, text, from_name)
    if "error" in result:
        return jsonify(result), 500
    
    return jsonify({"result": result})

@app.route('/tools/calendar', methods=['POST'])
def calendar_tool():
    data = request.get_json()
    year = data.get("year")
    month = data.get("month")
    
    result = get_month_calendar(year, month)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

@app.route('/tools/upcoming_dates', methods=['POST'])
def upcoming_dates_tool():
    data = request.get_json()
    date_type = data.get("date_type")
    count = data.get("count", 5)
    
    if not date_type:
        return jsonify({"error": "Date type is required"}), 400
    
    result = get_upcoming_dates(date_type, count)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

@app.route('/tools/tasks_add', methods=['POST'])
def tasks_add_tool():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    due_date = data.get("due_date")
    priority = data.get("priority", "medium")
    
    if not title:
        return jsonify({"error": "Task title is required"}), 400
    
    result = add_task(title, description, due_date, priority)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

@app.route('/tools/tasks_get', methods=['POST'])
def tasks_get_tool():
    data = request.get_json()
    filter_type = data.get("filter_type")
    
    result = get_tasks(filter_type)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

@app.route('/tools/tasks_update', methods=['POST'])
def tasks_update_tool():
    data = request.get_json()
    task_id = data.get("task_id")
    updates = data.get("updates", {})
    
    if task_id is None:
        return jsonify({"error": "Task ID is required"}), 400
    
    if not updates:
        return jsonify({"error": "No updates provided"}), 400
    
    result = update_task(task_id, updates)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

@app.route('/tools/tasks_delete', methods=['POST'])
def tasks_delete_tool():
    data = request.get_json()
    task_id = data.get("task_id")
    
    if task_id is None:
        return jsonify({"error": "Task ID is required"}), 400
    
    result = delete_task(task_id)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

@app.route('/tools/currency_convert', methods=['POST'])
def currency_convert_tool():
    data = request.get_json()
    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")
    amount = data.get("amount")
    
    if not from_currency or not to_currency or amount is None:
        return jsonify({"error": "Source currency, target currency, and amount are required"}), 400
    
    result = convert_currency(from_currency, to_currency, amount)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

@app.route('/tools/currency_rates', methods=['POST'])
def currency_rates_tool():
    data = request.get_json()
    base_currency = data.get("base_currency")
    
    if not base_currency:
        return jsonify({"error": "Base currency is required"}), 400
    
    result = get_exchange_rates(base_currency)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"result": result})

# Cursor Model Context Protocol endpoints
@app.route('/cursor/context/search', methods=['POST'])
def cursor_search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON request"}), 400
            
        result = cursor_provider.process_search(data)
        return jsonify(result)
    except Exception as e:
        print(f"Error in cursor search: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/cursor/context/retrieve', methods=['POST'])
def cursor_retrieve():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON request"}), 400
            
        result = cursor_provider.process_retrieve(data)
        return jsonify(result)
    except Exception as e:
        print(f"Error in cursor retrieve: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Main Cursor context endpoint (SSE and WebSocket)
@app.route('/cursor/context', methods=['GET', 'POST'])
def cursor_context():
    # If GET request, handle as SSE
    if request.method == 'GET':
        def generate():
            # Format exactly as required by Cursor's SSE client - using the format from the docs
            yield f"id: 1\nevent: message\ndata: {json.dumps({'type': 'connected'})}\n\n"
            
            # Just send the initial message, Cursor will reconnect as needed
            # We don't want an infinite loop here as it would block the server
                
        response = Response(generate(), mimetype="text/event-stream")
        response.headers.add('Cache-Control', 'no-cache')
        response.headers.add('Connection', 'keep-alive')
        return response
    
    # If POST request, handle like a regular API endpoint
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON request"}), 400
            
        # Determine what action to take based on the payload
        if "query" in data:
            # This is a search request
            return cursor_search()
        elif "urls" in data:
            # This is a retrieve request
            return cursor_retrieve()
        else:
            action = data.get("action", "")
            if action == "search":
                return cursor_search()
            elif action == "retrieve":
                return cursor_retrieve()
            else:
                return jsonify({"error": "Invalid request format"}), 400

# Add a simple health endpoint for Cursor
@app.route('/cursor/health', methods=['GET'])
def cursor_health():
    return jsonify({"status": "ok", "message": "MCP Server is running and ready to serve Cursor"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5734))  # Still allows PORT override for deployment
    print(f"Starting MCP Server on port {port}...")
    print(f"Cursor integration available at http://localhost:{port}/cursor/context")
    print(f"For Cursor integration, use this URL in Cursor settings: http://localhost:{port}/cursor/context")
    app.run(host="0.0.0.0", port=port, debug=True)