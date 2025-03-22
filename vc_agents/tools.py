# Import directly from the installed 'agents' package
from agents import function_tool
from services.search_service import SearchService
from services.scraping_service import ScrapingService
from typing import Dict, Any, List, Optional
import logging
import os
from e2b_code_interpreter import Sandbox

# Set up logging
logger = logging.getLogger(__name__)

@function_tool
async def run_python_code(code: str) -> str:
    """
    Execute Python code using E2B and return the results.
    
    Args:
        code: The Python code to execute
        
    Returns:
        The output of the executed code
    """
    logger.info(f"Tool called: run_python_code")
    
    try:
        # Create a sandbox
        with Sandbox() as sandbox:
            # Execute the code
            execution = sandbox.run_code(code)
            
            # Prepare the result
            result = ""
            
            # Add any stdout output
            if execution.logs and execution.logs.stdout:
                result += f"Output:\n{execution.logs.stdout}\n\n"
            
            # Add any stderr output
            if execution.logs and execution.logs.stderr:
                result += f"Errors:\n{execution.logs.stderr}\n\n"
                
            # Add the text result if available
            if execution.text:
                result += f"Result:\n{execution.text}\n\n"
                
            # Check for error
            if execution.error:
                result += f"Error:\n{execution.error.name}: {execution.error.value}\n"
                if hasattr(execution.error, 'traceback'):
                    result += f"Traceback:\n{execution.error.traceback}\n"
            
            # If there are any charts or visualizations, mention them
            if execution.results and any(r.png for r in execution.results):
                result += "Note: The code generated visualizations that can't be displayed in text format.\n"
            
            logger.info("Python code execution completed")
            return result if result else "Code executed successfully with no output."
    except Exception as e:
        error_message = f"Error executing Python code: {str(e)}"
        logger.exception(error_message)
        return f"Execution error: {error_message}"

@function_tool
async def search_google(query: str, num_results: int) -> str:
    """
    Search Google for information about a startup or topic.
    
    Args:
        query: The search query
        num_results: Number of results to return
    """
    logger.info(f"Tool called: search_google(query='{query}', num_results={num_results})")
    
    try:
        results = await SearchService.search(query, num_results)
        
        # Format results for the agent
        formatted_results = "Search results:\n\n"
        if not results:
            formatted_results += "No results found.\n"
        else:
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. {result['title']}\n"
                formatted_results += f"   URL: {result['link']}\n"
                formatted_results += f"   {result['snippet']}\n\n"
        
        logger.info(f"search_google returned {len(results)} results")
        return formatted_results
    except Exception as e:
        error_message = f"Error performing search for '{query}': {str(e)}"
        logger.exception(error_message)
        return f"Search error: {error_message}"

@function_tool
async def scrape_website(url: str, focus: Optional[str] = None) -> str:
    """
    Scrape content from a website.
    
    Args:
        url: The URL to scrape
        focus: Focus area (e.g., "about", "team", "investors")
    """
    logger.info(f"Tool called: scrape_website(url='{url}', focus='{focus}')")
    
    try:
        selectors = None
        if focus:
            # Define selectors based on focus area
            if focus == "team" or focus == "people":
                selectors = {
                    "team": ".team, .people, .leadership, .executives, [class*='team'], [class*='people']",
                    "leadership": ".leadership, .executives, .management, [class*='leadership']"
                }
            elif focus == "investors" or focus == "funding":
                selectors = {
                    "investors": ".investors, .funding, .backers, [class*='investor'], [class*='funding']"
                }
            elif focus == "about":
                selectors = {
                    "about": ".about, #about, [class*='about'], .company-info, #company-info"
                }
        
        result = await ScrapingService.scrape_website(url, selectors)
        
        if "error" in result:
            error_message = f"Error scraping {url}: {result['error']}"
            logger.error(error_message)
            return error_message
        
        # Format the result for the agent
        formatted_result = f"Content from {url}:\n\n"
        formatted_result += f"Title: {result['title']}\n\n"
        
        if result.get('description'):
            formatted_result += f"Description: {result['description']}\n\n"
        
        if focus and result.get('specific_content'):
            formatted_result += f"--- {focus.upper()} CONTENT ---\n\n"
            for key, texts in result['specific_content'].items():
                if isinstance(texts, list):
                    formatted_result += f"{key.capitalize()}:\n"
                    for text in texts:
                        formatted_result += f"- {text}\n"
                else:
                    formatted_result += f"{key.capitalize()}: {texts}\n"
            formatted_result += "\n"
        
        formatted_result += "--- MAIN CONTENT ---\n\n"
        formatted_result += result.get('content', 'No content extracted')
        
        logger.info(f"Successfully scraped {url}")
        return formatted_result
    except Exception as e:
        error_message = f"Error in scrape_website for '{url}': {str(e)}"
        logger.exception(error_message)
        return f"Scraping error: {error_message}"
