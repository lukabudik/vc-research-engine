# VC Research Engine

A FastAPI-based API for retrieving and researching startup data using AI agents with the OpenAI Agentic SDK.

## Overview

This project provides a REST API for:

- Retrieving startup data from Crunchbase (currently mocked)
- Performing AI-powered research on startups using the OpenAI Agentic SDK
- Orchestrating specialized research agents for comprehensive startup analysis
- Streaming research progress in real-time via WebSockets
- API key authentication for secure access

## Project Structure

```
vc-research-engine/
├── .env                    # Environment variables (API keys)
├── main.py                 # Main FastAPI application
├── requirements.txt        # Project dependencies
├── test_orchestrator.py    # Test script for the orchestrator
├── vc_agents/              # Agent modules
│   ├── __init__.py         # Makes vc_agents a Python package
│   ├── orchestrator.py     # Research orchestration system
│   ├── tools.py            # Agent tool implementations
│   ├── prompts.py          # Agent instructions and schemas
│   └── agents/             # Specialized agents
│       ├── __init__.py     # Makes agents a Python package
│       ├── company_agent.py   # Company overview agent
│       ├── people_agent.py    # Key people research agent
│       ├── market_agent.py    # Market analysis agent
│       ├── competitor_agent.py # Competitor analysis agent
│       └── metrics_agent.py   # Growth metrics agent
├── services/               # Service modules
│   ├── __init__.py         # Makes services a Python package
│   ├── crunchbase_service.py  # Service for Crunchbase data
│   ├── research_service.py    # Service for research functionality
│   ├── search_service.py      # Service for Google search
│   └── scraping_service.py    # Service for web scraping
└── venv/                   # Python virtual environment
```

## Prerequisites

- Python 3.8+
- OpenAI API key
- Serper API key (for Google search)

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Install Playwright browsers:
   ```
   playwright install chromium
   ```
5. Configure API keys in the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

## Running the API

Start the API server with:

```
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## Authentication

This API uses API key authentication. All endpoints (except the root endpoint) require an API key to be included in the request headers.

- **API Key Header**: `X-API-Key`
- **Default API Key**: `your-secret-api-key-12345` (hardcoded for development, should be changed in production)

Example of including the API key in a request:

```bash
curl -X POST "http://localhost:8000/getData" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-secret-api-key-12345" \
     -d '{"company_name": "OpenAI"}'
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Note: When using the Swagger UI to test endpoints, you'll need to click the "Authorize" button and enter the API key.

## API Endpoints

### Root Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Authentication**: None (public endpoint)
- **Description**: Health check endpoint
- **Response Example**:
  ```json
  {
    "status": "API is running",
    "endpoints": ["/getData", "/research", "/ws/research"],
    "authentication": "API Key required in X-API-Key header"
  }
  ```

### Get Data Endpoint

- **URL**: `/getData`
- **Method**: `POST`
- **Authentication**: Required (API Key in X-API-Key header)
- **Description**: Retrieve data about a startup from Crunchbase (currently mocked)
- **Request Body**:
  ```json
  {
    "company_name": "OpenAI"
  }
  ```
- **Response Example**:
  ```json
  {
    "name": "OpenAI",
    "description": "OpenAI is an AI research and deployment company...",
    "funding_rounds": [
      {
        "date": "2019-03-01",
        "amount": 1000000000,
        "series": "A",
        "investors": ["Microsoft"]
      }
    ],
    "founders": ["Sam Altman", "Elon Musk", "..."],
    "industry": "Artificial Intelligence",
    "founded_year": 2015,
    "total_funding": 3000000000,
    "website": "https://openai.com",
    "location": "San Francisco, CA",
    "status": "Operating"
  }
  ```

### Research Endpoint

- **URL**: `/research`
- **Method**: `POST`
- **Authentication**: Required (API Key in X-API-Key header)
- **Description**: Perform AI-powered research on a startup
- **Request Body**:
  ```json
  {
    "company_name": "OpenAI",
    "params": {
      "depth": "detailed",
      "focus_areas": ["tech_stack", "competitors"]
    }
  }
  ```
- **Response Example**:
  ```json
  {
    "company_info": {
      "name": "OpenAI",
      "description": "OpenAI is an AI research and deployment company...",
      "website": "https://openai.com",
      "founded_year": 2015,
      "location": "San Francisco, CA"
    },
    "dashboard_components": [
      {
        "id": "key-people",
        "title": "Key People",
        "type": "people",
        "size": "small",
        "data": [
          { "name": "Sam Altman", "role": "CEO", "avatar": "SA" },
          { "name": "Greg Brockman", "role": "President", "avatar": "GB" }
        ]
      },
      {
        "id": "tech-stack",
        "title": "Tech Stack",
        "type": "list",
        "size": "small",
        "data": [
          { "title": "Languages", "items": ["Python", "TypeScript", "C++"] },
          { "title": "Frameworks", "items": ["PyTorch", "TensorFlow"] }
        ]
      }
      // Additional components...
    ]
  }
  ```

### WebSocket Research Endpoint

- **URL**: `/ws/research`
- **Description**: WebSocket endpoint for streaming research progress
- **Initial Message**:
  ```json
  {
    "api_key": "your-secret-api-key-12345",
    "company_name": "OpenAI",
    "params": {
      "depth": "detailed"
    }
  }
  ```
- **Message Types**:
  - `start`: Research has started
  - `progress`: Progress update from the agent
  - `tool`: Tool usage notification
  - `complete`: Research is complete
  - `result`: Final research results
  - `error`: Error message

## Using the WebSocket Endpoint

Example JavaScript code to connect to the WebSocket endpoint:

```javascript
const socket = new WebSocket("ws://localhost:8000/ws/research");

socket.onopen = () => {
  // Send initial message with API key and company name
  socket.send(
    JSON.stringify({
      api_key: "your-secret-api-key-12345",
      company_name: "OpenAI",
      params: {
        depth: "detailed",
      },
    })
  );
};

socket.onmessage = (event) => {
  const message = JSON.parse(event.data);

  switch (message.type) {
    case "start":
      console.log("Research started:", message.message);
      break;
    case "progress":
      console.log("Progress:", message.message);
      break;
    case "tool":
      console.log("Tool usage:", message.message);
      break;
    case "complete":
      console.log("Research complete:", message.message);
      break;
    case "result":
      console.log("Final results:", message.data);
      // Process the dashboard data
      break;
    case "error":
      console.error("Error:", message.message);
      break;
  }
};

socket.onerror = (error) => {
  console.error("WebSocket error:", error);
};

socket.onclose = () => {
  console.log("WebSocket connection closed");
};
```

## Architecture

The VC Research Engine uses a modular architecture with specialized agents for different aspects of startup research:

### Research Orchestrator

The `ResearchOrchestrator` class in `vc_agents/orchestrator.py` coordinates the research process by:

1. Delegating research tasks to specialized agents
2. Collecting and combining results from each agent
3. Validating and formatting the final output

### Specialized Agents

Each specialized agent focuses on a specific aspect of startup research:

- **Company Overview Agent**: Researches basic company information, business model, and tech stack
- **Key People Agent**: Researches founders, executives, and key team members
- **Market Analysis Agent**: Analyzes TAM (Total Addressable Market) and SAM (Serviceable Addressable Market)
- **Competitor Analysis Agent**: Maps the competitive landscape and identifies competitive advantages
- **Growth Metrics Agent**: Researches growth metrics, funding, clients, and media presence

### Tools

The agents use several tools to gather information:

- **Google Search**: Uses the Serper API to search for information
- **Website Scraping**: Uses Playwright to extract content from websites

## Future Enhancements

- Implement actual Crunchbase API integration
- Add more agent tools (e.g., financial data APIs, news APIs)
- Enhance the research capabilities with additional specialized agents
- Implement full streaming support for the orchestrator
- Add more robust error handling and rate limiting
- Add user authentication and personalized research profiles
- Implement caching for common research queries
