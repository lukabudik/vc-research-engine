from typing import Dict, Any, List, Optional, Union
import os
import json
import asyncio
import jsonschema
from pydantic import BaseModel
from fastapi import WebSocket

# Import from our local modules
from vc_agents.orchestrator import ResearchOrchestrator
from vc_agents.prompts import RESEARCH_OUTPUT_SCHEMA

def validate_research_output(data: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
    """
    Validate the research output against the expected schema
    
    Args:
        data: The JSON data to validate
        
    Returns:
        Dictionary with validation result and error message if any
    """
    try:
        jsonschema.validate(instance=data, schema=RESEARCH_OUTPUT_SCHEMA)
        return {"valid": True, "message": ""}
    except jsonschema.exceptions.ValidationError as e:
        return {"valid": False, "message": str(e)}
    except Exception as e:
        return {"valid": False, "message": f"Unexpected validation error: {str(e)}"}

class ResearchParams(BaseModel):
    depth: Optional[str] = "standard"  # standard, detailed
    focus_areas: Optional[List[str]] = None

class ResearchService:
    """
    Service for performing research on startups using AI agents
    """
    
    @staticmethod
    async def perform_research(
        company_name: str, 
        research_params: Dict[str, Any] = None,
        websocket: Optional[WebSocket] = None
    ) -> Dict[str, Any]:
        """
        Perform research on a startup using AI agents
        
        Args:
            company_name: Name of the company to research
            research_params: Optional parameters to customize the research
            websocket: Optional WebSocket for streaming progress updates
            
        Returns:
            Dictionary containing research results
        """
        params = ResearchParams(**(research_params or {}))
        
        # Create the research orchestrator
        orchestrator = ResearchOrchestrator(model="gpt-4o")
        
        # If websocket is provided, we need to implement streaming
        if websocket:
            await websocket.send_text(json.dumps({
                "type": "start",
                "message": f"Starting research on {company_name}..."
            }))
            
            # Send initial phase message
            await websocket.send_text(json.dumps({
                "type": "phase",
                "message": "Initializing research orchestrator"
            }))
            
            # TODO: Implement streaming with the orchestrator
            # For now, we'll just run the research and send periodic updates
            
            # Send company overview phase message
            await websocket.send_text(json.dumps({
                "type": "phase",
                "message": "Researching company overview"
            }))
            
            # Send key people phase message
            await websocket.send_text(json.dumps({
                "type": "phase",
                "message": "Analyzing key people"
            }))
            
            # Send market analysis phase message
            await websocket.send_text(json.dumps({
                "type": "phase",
                "message": "Analyzing market size (TAM/SAM)"
            }))
            
            # Send competitor analysis phase message
            await websocket.send_text(json.dumps({
                "type": "phase",
                "message": "Mapping competitive landscape"
            }))
            
            # Send growth metrics phase message
            await websocket.send_text(json.dumps({
                "type": "phase",
                "message": "Researching growth metrics and media presence"
            }))
            
            # Run the research
            result = await orchestrator.research_startup(company_name, params.model_dump())
            
            # Send completion message
            await websocket.send_text(json.dumps({
                "type": "complete",
                "message": "Research complete!"
            }))
            
            return result
        else:
            # Run the research without streaming
            return await orchestrator.research_startup(company_name, params.model_dump())
