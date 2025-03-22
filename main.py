from fastapi import FastAPI, HTTPException, Depends, Header, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import secrets

from services.crunchbase_service import CrunchbaseService
from services.research_service import ResearchService

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

# Root endpoint for API health check (no authentication required)
@app.get("/")
async def root():
    return {
        "status": "API is running", 
        "endpoints": ["/getData", "/research"],
        "authentication": f"API Key required in {API_KEY_NAME} header"
    }

# Run the application with uvicorn when this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
