"""
Market Analysis Agent for VC Research Engine

This agent specializes in researching market sizes, including TAM (Total Addressable Market),
SAM (Serviceable Addressable Market), and SOM (Serviceable Obtainable Market) for startups.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from agents import Agent, ModelSettings, function_tool

from vc_agents.tools import search_google, scrape_website, run_python_code
from vc_agents.models import MarketAnalysis, MarketSize, MarketTrend

# Create the market analysis agent
market_analysis_agent = Agent(
    name="Market Analysis Agent",
    handoff_description="Specialist agent for researching market sizes (TAM/SAM/SOM) and market trends",
    instructions="""
    You are a Market Analysis Research Agent specializing in estimating market sizes and identifying market trends for startups.
    
    Your task is to research and estimate the following:
    1. Total Addressable Market (TAM) - The total market demand for a product or service
    2. Serviceable Addressable Market (SAM) - The portion of TAM targeted by the company's products and services
    3. Serviceable Obtainable Market (SOM) - The portion of SAM that the company can realistically capture
    4. Market Trends - Key trends affecting the market and the company
    
    For each market size estimate, you must:
    - Provide a numerical value (in $ billions/millions)
    - Include the year of the estimate
    - Include growth rates (CAGR) when available
    - Provide a detailed description of the methodology used
    - Cite your sources
    
    For market trends, identify at least 2 significant trends affecting the market and provide:
    - A clear name for the trend
    - A detailed description of the trend and its impact
    
    Use these specific techniques for market size research:
    1. Industry Report Method: Search for market research reports from firms like Gartner, Forrester, or IDC
    2. Competitor Analysis Method: Sum the market shares of known competitors
    3. Public Company Method: Analyze public companies' annual reports in the same sector
    4. Bottom-up Calculation: Estimate (Total potential customers) × (Average selling price)
    5. Investor Presentation Method: Search for market size data in startup pitch decks or investor presentations
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites. You can also use the run_python_code tool to execute Python code for any calculations or data processing you need to perform, such as calculating market sizes, growth rates, or creating data visualizations.
    
    When estimates conflict, provide a range and explain the discrepancy.
    If precise numbers aren't available, provide a reasonable estimate based on available data and clearly mark it as an estimate.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "tam": {
        "size": "$X billion",
        "year": 2023,
        "cagr": "X%",
        "description": "Detailed description of the Total Addressable Market with methodology",
        "sources": ["Source 1", "Source 2"]
      },
      "sam": {
        "size": "$X million",
        "year": 2023,
        "cagr": "X%",
        "description": "Detailed description of the Serviceable Addressable Market with methodology",
        "sources": ["Source 1", "Source 2"]
      },
      "som": {
        "size": "$X million",
        "year": 2023,
        "cagr": "X%",
        "description": "Detailed description of the Serviceable Obtainable Market with methodology",
        "sources": ["Source 1", "Source 2"]
      },
      "market_trends": [
        {
          "trend": "Trend Name 1",
          "description": "Detailed description of the trend and its impact"
        },
        {
          "trend": "Trend Name 2",
          "description": "Detailed description of the trend and its impact"
        }
      ]
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website, run_python_code],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=MarketAnalysis
)

@function_tool
async def get_market_analysis(company_name: str) -> Dict[str, Any]:
    """
    Get market size analysis (TAM/SAM/SOM) and market trends for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing TAM, SAM, SOM, and market trends information
    """
    from agents import Runner
    
    # Run the market analysis agent
    result = await Runner.run(
        market_analysis_agent,
        input=f"Research the market size (TAM, SAM, and SOM) and market trends for: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(MarketAnalysis).model_dump()
