"""
Research Orchestrator for VC Research Engine

This module implements a research orchestration system using the OpenAI Agentic SDK.
It coordinates specialized agents for different aspects of startup research.
"""

from typing import Dict, Any, List, Optional, Union
import json
import asyncio
from datetime import datetime
from pydantic import BaseModel, Field

from agents import Agent, Runner, ModelSettings, function_tool, handoff
from vc_agents.prompts import RESEARCH_AGENT_INSTRUCTIONS, RESEARCH_OUTPUT_SCHEMA
from vc_agents.models import ResearchOutput

# Import specialized agents
from vc_agents.agents.company_agent import company_overview_agent, get_company_overview
from vc_agents.agents.people_agent import key_people_agent, get_team_analysis
from vc_agents.agents.market_agent import market_analysis_agent, get_market_analysis
from vc_agents.agents.competitor_agent import competitor_analysis_agent, get_competitor_analysis
from vc_agents.agents.metrics_agent import (
    growth_metrics_agent, get_growth_metrics,
    financial_metrics_agent, get_financial_metrics,
    product_analysis_agent, get_product_analysis,
    customer_analysis_agent, get_customer_analysis,
    risk_assessment_agent, get_risk_assessment,
    investment_analysis_agent, get_investment_analysis,
    media_news_agent, get_media_news,
    research_metadata_agent, get_research_metadata
)


class ResearchOrchestrator:
    """
    Orchestrates the research process using specialized agents for different aspects
    of startup research.
    """
    
    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize the research orchestrator.
        
        Args:
            model: The model to use for the main orchestrator agent
        """
        self.model = model
    
    async def research_startup(self, company_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive research on a startup.
        
        Args:
            company_name: The name of the startup to research
            params: Optional parameters to customize the research
            
        Returns:
            A dictionary containing the research results
        """
        try:
            print(f"Starting research on {company_name}...")
            
            # Step 1: Get company overview
            print("Step 1: Getting company overview...")
            from vc_agents.agents.company_agent import company_overview_agent
            company_result = await Runner.run(
                company_overview_agent,
                input=f"Research basic information about the company: {company_name}"
            )
            company_data = company_result.final_output_as(dict)
            
            # Step 2: Get team analysis
            print("Step 2: Researching team analysis...")
            from vc_agents.agents.people_agent import key_people_agent
            team_result = await Runner.run(
                key_people_agent,
                input=f"Research the team (founders, executives, board members, and advisors) of: {company_name}"
            )
            team_data = team_result.final_output_as(dict)
            
            # Step 3: Get market analysis
            print("Step 3: Analyzing market size...")
            from vc_agents.agents.market_agent import market_analysis_agent
            market_result = await Runner.run(
                market_analysis_agent,
                input=f"Research the market size (TAM, SAM, and SOM) and market trends for: {company_name}"
            )
            market_data = market_result.final_output_as(dict)
            
            # Step 4: Get financial metrics
            print("Step 4: Analyzing financial metrics...")
            from vc_agents.agents.metrics_agent import financial_metrics_agent
            financial_result = await Runner.run(
                financial_metrics_agent,
                input=f"Research the financial metrics for: {company_name}"
            )
            financial_data = financial_result.final_output_as(dict)
            
            # Step 5: Get growth metrics
            print("Step 5: Researching growth metrics...")
            from vc_agents.agents.metrics_agent import growth_metrics_agent
            growth_result = await Runner.run(
                growth_metrics_agent,
                input=f"Research the growth metrics for: {company_name}"
            )
            growth_data = growth_result.final_output_as(dict)
            
            # Step 6: Get competitive landscape
            print("Step 6: Mapping competitive landscape...")
            from vc_agents.agents.competitor_agent import competitor_analysis_agent
            competitor_result = await Runner.run(
                competitor_analysis_agent,
                input=f"Research the competitors and competitive landscape for: {company_name}"
            )
            competitor_data = competitor_result.final_output_as(dict)
            
            # Step 7: Get product analysis
            print("Step 7: Analyzing product...")
            from vc_agents.agents.metrics_agent import product_analysis_agent
            product_result = await Runner.run(
                product_analysis_agent,
                input=f"Research the product(s) of: {company_name}"
            )
            product_data = product_result.final_output_as(dict)
            
            # Step 8: Get customer analysis
            print("Step 8: Analyzing customers...")
            from vc_agents.agents.metrics_agent import customer_analysis_agent
            customer_result = await Runner.run(
                customer_analysis_agent,
                input=f"Research the customers and clients of: {company_name}"
            )
            customer_data = customer_result.final_output_as(dict)
            
            # Step 9: Get risk assessment
            print("Step 9: Assessing risks...")
            from vc_agents.agents.metrics_agent import risk_assessment_agent
            risk_result = await Runner.run(
                risk_assessment_agent,
                input=f"Research the risks for: {company_name}"
            )
            risk_data = risk_result.final_output_as(dict)
            
            # Step 10: Get investment analysis
            print("Step 10: Analyzing investment potential...")
            from vc_agents.agents.metrics_agent import investment_analysis_agent
            investment_result = await Runner.run(
                investment_analysis_agent,
                input=f"Research the investment potential of: {company_name}"
            )
            investment_data = investment_result.final_output_as(dict)
            
            # Step 11: Get media and news
            print("Step 11: Gathering media and news...")
            from vc_agents.agents.metrics_agent import media_news_agent
            media_result = await Runner.run(
                media_news_agent,
                input=f"Research the media coverage and news for: {company_name}"
            )
            media_data = media_result.final_output_as(dict)
            
            # Step 12: Get research metadata
            print("Step 12: Creating research metadata...")
            from vc_agents.agents.metrics_agent import research_metadata_agent
            metadata_result = await Runner.run(
                research_metadata_agent,
                input=f"Create research metadata for: {company_name}"
            )
            metadata_data = metadata_result.final_output_as(dict)
            
            # Combine all results into a single output
            combined_data = {
                "company_info": company_data,
                "market_analysis": market_data,
                "financial_metrics": financial_data,
                "growth_metrics": growth_data,
                "competitive_landscape": competitor_data,
                "team_analysis": team_data,
                "product_analysis": product_data,
                "customer_analysis": customer_data,
                "risk_assessment": risk_data,
                "investment_analysis": investment_data,
                "media_and_news": media_data,
                "research_metadata": metadata_data
            }
            
            # Validate the combined data
            try:
                validated_data = ResearchOutput(**combined_data)
                return validated_data.model_dump()
            except Exception as e:
                print(f"Warning: Validation error: {str(e)}")
                # Return the data anyway, even if it doesn't fully validate
                return combined_data
            
        except Exception as e:
            # Catch any errors during the research process
            print(f"Error during research: {str(e)}")
            return {
                "error": f"Error during research: {str(e)}"
            }
