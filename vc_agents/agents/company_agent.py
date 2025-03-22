"""
Company Overview Agent for VC Research Engine

This agent specializes in gathering basic information about companies,
including description, website, founding year, and location.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from agents import Agent, ModelSettings, function_tool

from vc_agents.tools import search_google, scrape_website, run_python_code
from vc_agents.models import CompanyInfo

# Create the company overview agent
company_overview_agent = Agent(
    name="Company Overview Agent",
    handoff_description="Specialist agent for gathering basic company information",
    instructions="""
    You are a Company Overview Research Agent specializing in gathering basic information about startups.
    
    Your task is to research and collect the following information:
    1. Company name (official name)
    2. Company tagline (short description or slogan)
    3. Company description (comprehensive description of what they do)
    4. Company website (official URL)
    5. Founding year (when the company was founded)
    6. Headquarters location (city, state/country)
    7. Company stage (e.g., Seed, Series A, Series B, etc.)
    8. Employee count (approximate number of employees)
    9. Business model (how the company makes money)
    10. Revenue model (e.g., SaaS, Enterprise Sales, etc.)
    11. Industry (main industry or sector)
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites. You can also use the run_python_code tool to execute Python code for any calculations or data processing you need to perform.
    
    Focus on authoritative sources like:
    - The company's official website
    - LinkedIn company page
    - Crunchbase profile
    - Tech blogs and news articles
    
    For each piece of information, cite your source and explain how you determined it.
    If you cannot find specific information, indicate that it's not available and provide your best estimate if possible.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "name": "Name of the company",
      "tagline": "Short company tagline or slogan",
      "description": "Comprehensive description of what the company does",
      "website": "https://company-website.com",
      "founded_year": 2020,
      "headquarters": "City, State/Country",
      "company_stage": "Series A",
      "employee_count": 50,
      "business_model": "B2B",
      "revenue_model": "SaaS/Enterprise Sales",
      "industry": "AI/Machine Learning"
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website, run_python_code],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=CompanyInfo
)

@function_tool
async def get_company_overview(company_name: str) -> Dict[str, Any]:
    """
    Get comprehensive overview information about a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing basic company information
    """
    from agents import Runner
    
    # Run the company overview agent
    result = await Runner.run(
        company_overview_agent,
        input=f"Research basic information about the company: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(CompanyInfo).model_dump()
