"""
Team Analysis Agent for VC Research Engine

This agent specializes in researching founders, executives, key team members,
board members, and advisors of startups, including their backgrounds and roles.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from agents import Agent, ModelSettings, function_tool

from vc_agents.tools import search_google, scrape_website, run_python_code
from vc_agents.models import TeamAnalysis, Person, BoardMember, Advisor

# Create the team analysis agent
key_people_agent = Agent(
    name="Team Analysis Agent",
    handoff_description="Specialist agent for researching founders, executives, board members, and advisors",
    instructions="""
    You are a Team Analysis Research Agent specializing in gathering information about founders, 
    executives, board members, advisors, and key team members of startups.
    
    Your task is to research and collect the following information:
    
    1. Key People (Founders and Executives):
       - Name (full name)
       - Role (current position at the company)
       - Background (previous companies, education, relevant experience)
       - LinkedIn profile URL (if available)
    
    2. Board Members:
       - Name (full name)
       - Role on the board
       - Organization they represent
       - Background (relevant experience)
    
    3. Advisors:
       - Name (full name)
       - Role or area of expertise
       - Background (relevant experience)
    
    4. Team Strength:
       - An overall assessment of the team's strengths, experience, and capabilities
    
    Focus on:
    - Founders
    - C-level executives (CEO, CTO, CFO, etc.)
    - Board members
    - Key advisors
    - Other significant team members
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites. You can also use the run_python_code tool to execute Python code for any calculations or data processing you need to perform, such as analyzing team composition, extracting patterns from career histories, or processing data about team members.
    
    Focus on authoritative sources like:
    - The company's official website (team/about pages)
    - LinkedIn profiles
    - Crunchbase profiles
    - Tech blogs and news articles
    - Conference speaker bios
    
    For each person, cite your source and explain how you determined their information.
    If you cannot find specific information, indicate that it's not available.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "key_people": [
        {
          "name": "Person Name",
          "role": "CEO",
          "background": "Brief background including previous companies and experience",
          "linkedin": "https://www.linkedin.com/in/person-name"
        }
      ],
      "board_members": [
        {
          "name": "Board Member Name",
          "role": "Board Member",
          "organization": "Organization Name",
          "background": "Brief background"
        }
      ],
      "advisors": [
        {
          "name": "Advisor Name",
          "role": "Advisor",
          "background": "Brief background"
        }
      ],
      "team_strength": "Overall assessment of the team's strengths, experience, and capabilities"
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    
    Aim to find at least 3-5 key people, prioritizing founders and C-level executives.
    """,
    tools=[search_google, scrape_website, run_python_code],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=TeamAnalysis
)

@function_tool
async def get_team_analysis(company_name: str) -> Dict[str, Any]:
    """
    Get comprehensive team analysis including key people, board members, and advisors of a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing information about the team
    """
    from agents import Runner
    
    # Run the team analysis agent
    result = await Runner.run(
        key_people_agent,
        input=f"Research the team (founders, executives, board members, and advisors) of: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(TeamAnalysis).model_dump()
