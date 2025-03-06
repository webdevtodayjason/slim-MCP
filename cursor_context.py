import requests
import json
from bs4 import BeautifulSoup
import re
import os

class CursorContextProvider:
    """Handler for Cursor Model Context Protocol requests."""
    
    def __init__(self):
        """Initialize the context provider with default settings."""
        self.search_limit = 5  # Number of search results to return
        self.content_max_length = 10000  # Max length for content retrieval
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    
    def search(self, query):
        """
        Search for content based on a query.
        
        Args:
            query (str): The search query
            
        Returns:
            list: Search result items
        """
        if not query:
            return []
            
        results = []
        try:
            # Try DuckDuckGo first
            url = f"https://duckduckgo.com/html/?q={query}"
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                for result in soup.find_all("div", class_="result__body", limit=self.search_limit):
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
            
        return results
    
    def retrieve_content(self, urls):
        """
        Retrieve content from specified URLs.
        
        Args:
            urls (list): List of URLs to retrieve
            
        Returns:
            list: Content items
        """
        if not urls:
            return []
            
        items = []
        for url in urls:
            try:
                headers = {"User-Agent": self.user_agent}
                response = requests.get(url, headers=headers, timeout=10)
                
                # Create a basic summary if HTML
                content = response.text
                
                # Handle different content types
                content_type = response.headers.get('Content-Type', '')
                
                if 'text/html' in content_type:
                    # HTML content
                    soup = BeautifulSoup(content, "html.parser")
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.extract()
                    
                    # Get the main content (prioritize article, main, or body)
                    main_content = soup.find('article') or soup.find('main') or soup.find('body')
                    if main_content:
                        content = main_content.get_text(separator='\n', strip=True)
                    else:
                        content = soup.get_text(separator='\n', strip=True)
                    
                    # Clean up whitespace
                    content = re.sub(r'\n+', '\n', content)
                    content = re.sub(r'\s+', ' ', content)
                    
                elif 'application/json' in content_type:
                    # Format JSON nicely
                    try:
                        json_data = json.loads(content)
                        content = json.dumps(json_data, indent=2)
                    except:
                        pass
                
                # Limit content size
                if len(content) > self.content_max_length:
                    content = content[:self.content_max_length] + "... (content truncated)"
                
                items.append({
                    "url": url,
                    "content": content
                })
            except Exception as e:
                items.append({
                    "url": url,
                    "error": str(e)
                })
        
        return items
    
    def process_search(self, data):
        """Process a search request."""
        query = data.get("query", "")
        return {
            "items": self.search(query)
        }
    
    def process_retrieve(self, data):
        """Process a retrieve request."""
        urls = data.get("urls", [])
        return {
            "items": self.retrieve_content(urls)
        }