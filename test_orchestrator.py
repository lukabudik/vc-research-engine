"""
Test script for the VC Research Engine Orchestrator

This script tests the ResearchOrchestrator by researching a sample startup.
"""

import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from vc_agents.orchestrator import ResearchOrchestrator

async def test_research_orchestrator():
    """Test the ResearchOrchestrator with a sample startup"""
    
    # Create the orchestrator
    orchestrator = ResearchOrchestrator(model="gpt-4o")
    
    # Sample startup to research
    company_name = "Anthropic"
    
    print(f"Starting research on {company_name}...")
    
    # Run the research
    result = await orchestrator.research_startup(
        company_name=company_name,
        params={
            "depth": "standard",
            "focus_areas": ["technology", "funding"]
        }
    )
    
    # Print the result
    print("\nResearch Results:")
    
    # Check if the result is a dictionary or a Pydantic model
    if hasattr(result, "model_dump"):
        # If it's a Pydantic model, convert it to a dictionary
        result_dict = result.model_dump()
        print(json.dumps(result_dict, indent=2))
        return result_dict
    elif isinstance(result, dict):
        # If it's already a dictionary, just print it
        print(json.dumps(result, indent=2))
        return result
    else:
        # If it's something else, just print its string representation
        print(str(result))
        return result

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_research_orchestrator())
