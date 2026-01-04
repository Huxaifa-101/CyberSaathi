"""
Web Search Tool - Tavily Integration
Searches the web for current information not in the database
"""
import logging
from langchain.tools import tool
from tavily import TavilyClient
from config import Config

logger = logging.getLogger(__name__)


@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for current information about Pakistani cyber laws and cybercrime.
    
    Use this tool when:
    - The user asks about recent cases or news
    - Information is not available in the law database
    - The query is about current events or updates
    - The user explicitly asks to search the web
    
    Args:
        query: The search query
    
    Returns:
        Web search results with sources
    """
    try:
        # Initialize Tavily client
        client = TavilyClient(api_key=Config.TAVILY_API_KEY)
        
        # Perform search
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
            include_raw_content=False
        )
        
        # Format results
        if response.get('answer'):
            result = f"**Summary:** {response['answer']}\n\n"
        else:
            result = ""
        
        result += "**Sources:**\n\n"
        
        for i, item in enumerate(response.get('results', []), 1):
            title = item.get('title', 'No title')
            url = item.get('url', '')
            content = item.get('content', 'No content available')
            
            result += f"{i}. **{title}**\n"
            result += f"   {content}\n"
            result += f"   Source: {url}\n\n"
        
        if not response.get('results'):
            result = "No web results found for this query."
        
        logger.info(f"Web search completed for query: {query[:50]}...")
        return result
    
    except Exception as e:
        logger.error(f"Error in web search: {e}")
        return f"Error performing web search: {str(e)}"
