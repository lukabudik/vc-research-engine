from fastapi import FastAPI, HTTPException, Depends, Header, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import secrets
import os

from services.crunchbase_service import CrunchbaseService
from services.research_service import ResearchService
from chatbot import chatbot_generate

# API Key configuration
# In a production environment, this should be stored securely (e.g., environment variables)
API_KEY = "your-secret-api-key-12345"
API_KEY_NAME = "X-API-Key"

# API Key security scheme
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Dependency to validate API key
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail="API Key is missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key

# Initialize FastAPI app
app = FastAPI(
    title="VC Research Engine",
    description="API for retrieving and researching startup data",
    version="0.1.0"
)

# Sample response model for getData endpoint
class StartupData(BaseModel):
    name: str
    description: str
    funding_rounds: List[Dict[str, Any]]
    founders: List[str]
    industry: str
    founded_year: int
    total_funding: float
    website: str
    location: str
    status: str


# Request model for getData endpoint
class GetDataRequest(BaseModel):
    company_name: str

@app.post("/getData", response_model=StartupData)
async def get_data(request: GetDataRequest, api_key: APIKey = Depends(get_api_key)):
    """
    Retrieve data about a startup from Crunchbase
    """
    try:
        data = await CrunchbaseService.get_startup_data(request.company_name)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")

# Request model for research endpoint
class ResearchRequest(BaseModel):
    company_name: str
    params: Optional[Dict[str, Any]] = None

@app.post("/research")
async def research(request: ResearchRequest, api_key: APIKey = Depends(get_api_key)):
    """
    Perform research on a startup
    This is currently a placeholder for future implementation
    """
    try:
        result = await ResearchService.perform_research(request.company_name, request.params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing research: {str(e)}")

# Request model for the chatbot endpoint
class ChatbotRequest(BaseModel):
    query: str
    research_json: dict
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "What is the most recent funding size?",
                    "research_json": {
                        "name": "Anthropic",
                        "description": "Anthropic is an AI safety company working to build reliable, interpretable, and steerable AI systems.",
                        "funding_rounds": [
                            {"date": "2021-05-01", "amount": 124000000, "series": "A", "investors": ["Jaan Tallinn", "Dustin Moskovitz"]},
                            {"date": "2022-04-15", "amount": 580000000, "series": "B", "investors": ["Google", "Spark Capital"]}
                        ],
                        "founders": ["Dario Amodei", "Daniela Amodei", "Tom Brown"],
                        "industry": "Artificial Intelligence",
                        "founded_year": 2021,
                        "total_funding": 704000000,
                        "website": "https://www.anthropic.com",
                        "location": "San Francisco, CA",
                        "status": "Operating"
                    }
                }
            ]
        }
    }


# Response model for the chatbot endpoint
class ChatbotResponse(BaseModel):
    response: str
    visualization: Optional[Dict[str, Any]] = None

@app.post("/ask_chatbot", response_model=ChatbotResponse)
async def ask_question(request: ChatbotRequest):
    """
    Ask a question about startup data
    
    This endpoint processes a user query about a specific company using the AI chatbot.
    It returns a text response and optional visualization data.
    """
    try:
        # Process the query using our chatbot
        response_text, visualization_data = await chatbot_generate(request.query, request.research_json)
        
        # Return the response
        return ChatbotResponse(
            response=response_text,
            visualization=visualization_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Root endpoint for API health check (no authentication required)
@app.get("/")
async def root():
    return {
        "status": "API is running", 
        "endpoints": ["/getData", "/research", "/ask_chatbot"],
        "authentication": f"API Key required in {API_KEY_NAME} header"
    }

# Run the application with uvicorn when this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
