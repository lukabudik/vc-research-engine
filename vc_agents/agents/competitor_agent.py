"""
Competitor Analysis Agent for VC Research Engine

This agent specializes in researching competitors and competitive landscape
for startups, including direct and indirect competitors.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from agents import Agent, ModelSettings, function_tool

from vc_agents.tools import search_google, scrape_website, run_python_code
from vc_agents.models import CompetitiveLandscape, Competitor, IndirectCompetitor, ComparisonChart, CompanyComparison

# Create the competitor analysis agent
competitor_analysis_agent = Agent(
    name="Competitor Analysis Agent",
    handoff_description="Specialist agent for researching competitors and competitive landscape",
    instructions="""
    You are a Competitor Analysis Research Agent specializing in mapping the competitive landscape for startups.
    
    Your task is to research and identify:
    1. Direct competitors - Companies offering similar products/services to the same target market
    2. Indirect competitors - Companies solving the same problem but with different approaches or targeting different segments
    3. Competitive advantages - What differentiates the company from its competitors
    4. Comparison chart - A feature/attribute comparison between the company and its competitors
    
    For the competitive landscape analysis:
    - Identify at least 2-3 direct competitors with detailed information
    - Identify at least 2-3 indirect competitors with basic information
    - Analyze the company's competitive advantages and differentiators
    - Create a comparison chart with 4-5 key categories/features
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites. You can also use the run_python_code tool to execute Python code for any calculations or data processing you need to perform, such as analyzing competitor data, calculating market shares, or creating comparison matrices.
    
    Focus on authoritative sources like:
    - The company's official website (especially comparison pages)
    - Competitor websites
    - Industry reports and analyses
    - Tech blogs and news articles
    - Review sites and comparison platforms
    
    For direct competitors, provide:
    - Name
    - Description of their offering
    - Funding information
    - Key strengths (at least 2-3)
    - Key weaknesses (at least 2-3)
    
    For indirect competitors, provide:
    - Name
    - Description of their offering
    - Funding information
    
    For the competitive advantage, provide a detailed analysis of what makes the company unique.
    
    For the comparison chart, include:
    - A title for the chart
    - 4-5 categories for comparison (e.g., features, pricing, target market)
    - Values for each company across these categories
    
    Your final output MUST be a JSON object with the following structure:
    {
      "direct_competitors": [
        {
          "name": "Competitor Name",
          "description": "Description of what they do",
          "funding": "$X million",
          "strengths": ["Strength 1", "Strength 2", "Strength 3"],
          "weaknesses": ["Weakness 1", "Weakness 2", "Weakness 3"]
        }
      ],
      "indirect_competitors": [
        {
          "name": "Competitor Name",
          "description": "Description of what they do",
          "funding": "$X million"
        }
      ],
      "competitive_advantage": "Detailed description of the company's competitive advantage",
      "comparison_chart": {
        "title": "Competitive Feature Comparison",
        "categories": ["Category 1", "Category 2", "Category 3", "Category 4"],
        "companies": [
          {
            "name": "Target Company",
            "values": ["Value 1", "Value 2", "Value 3", "Value 4"]
          },
          {
            "name": "Competitor 1",
            "values": ["Value 1", "Value 2", "Value 3", "Value 4"]
          }
        ]
      }
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website, run_python_code],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=CompetitiveLandscape
)

@function_tool
async def get_competitor_analysis(company_name: str) -> Dict[str, Any]:
    """
    Get competitor analysis for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing competitor analysis information
    """
    from agents import Runner
    
    # Run the competitor analysis agent
    result = await Runner.run(
        competitor_analysis_agent,
        input=f"Research the competitors and competitive landscape for: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(CompetitiveLandscape).model_dump()
