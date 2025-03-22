import os
import http.client
import json
import logging
from typing import Dict, Any, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchService:
    """Service for performing Google searches using Serper API"""
    
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    SERPER_HOST = "google.serper.dev"
    
    @staticmethod
    async def search(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a Google search using Serper API
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        if not SearchService.SERPER_API_KEY:
            logger.error("SERPER_API_KEY is not set in environment variables")
            return [{"title": "Error", "link": "", "snippet": "API key not configured"}]
        
        try:
            headers = {
                "X-API-KEY": SearchService.SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            
            payload = json.dumps({
                "q": query,
                "num": num_results
            })
            
            logger.info(f"Searching for: {query}")
            
            conn = http.client.HTTPSConnection(SearchService.SERPER_HOST)
            conn.request("POST", "/search", payload, headers)
            
            response = conn.getresponse()
            response_data = response.read().decode('utf-8')
            
            if response.status != 200:
                logger.error(f"Search API error: {response_data}")
                return [{"title": "Error", "link": "", "snippet": f"API error: {response.status}"}]
                
            data = json.loads(response_data)
            
            results = []
            if "organic" in data:
                for item in data["organic"][:num_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })
            
            logger.info(f"Found {len(results)} results")
            
            conn.close()
            return results
        except Exception as e:
            logger.exception(f"Error in search: {str(e)}")
            return [{"title": "Error", "link": "", "snippet": f"Search failed: {str(e)}"}]
