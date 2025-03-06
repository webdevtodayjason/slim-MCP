#!/usr/bin/env python3
"""
Simple Cursor Context Protocol server.
This is a minimal implementation focused solely on the Cursor Context Protocol.
"""

from flask import Flask, Response, request, jsonify
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path=""):
    return Response("", status=200)

# Main SSE endpoint that Cursor connects to
@app.route('/cursor/context', methods=['GET'])
def cursor_context_stream():
    def generate():
        # Send a single message to indicate connection
        yield f"event: message\ndata: {json.dumps({'type': 'connected'})}\n\n"
    
    response = Response(generate(), mimetype="text/event-stream")
    response.headers.add('Cache-Control', 'no-cache')
    response.headers.add('Connection', 'keep-alive')
    return response

# Search endpoint that Cursor calls
@app.route('/cursor/context/search', methods=['POST'])
def cursor_search():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"items": []})
    
    # Simple search implementation using DuckDuckGo
    results = []
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            for result in soup.find_all("div", class_="result__body", limit=5):
                title = result.find("a", class_="result__a").text if result.find("a", class_="result__a") else "No title"
                snippet = result.find("div", class_="result__snippet").text if result.find("div", class_="result__snippet") else "No snippet"
                link = result.find("a", class_="result__a")['href'] if result.find("a", class_="result__a") else "#"
                
                results.append({
                    "title": title,
                    "content": snippet,
                    "url": link
                })
    except Exception as e:
        print(f"Search error: {str(e)}")
    
    return jsonify({"items": results})

# Retrieve endpoint that Cursor calls to get content from URLs
@app.route('/cursor/context/retrieve', methods=['POST'])
def cursor_retrieve():
    data = request.get_json()
    urls = data.get('urls', [])
    
    if not urls:
        return jsonify({"items": []})
    
    items = []
    for url in urls:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            content = response.text
            if 'text/html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(content, "html.parser")
                for script in soup(["script", "style"]):
                    script.extract()
                content = soup.get_text(separator='\n', strip=True)
                
                # Limit content length
                if len(content) > 8000:
                    content = content[:8000] + "... (content truncated)"
            
            items.append({
                "url": url,
                "content": content
            })
        except Exception as e:
            items.append({
                "url": url,
                "error": str(e)
            })
    
    return jsonify({"items": items})

if __name__ == '__main__':
    print("Starting Cursor Context Protocol server on port 5734...")
    print("For Cursor integration, use this URL: http://localhost:5734/cursor/context")
    app.run(host='0.0.0.0', port=5734, debug=True)