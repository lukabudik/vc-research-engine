# VC Research Engine

A FastAPI-based API for retrieving and researching startup data.

## Overview

This project provides a REST API for:

- Retrieving startup data from Crunchbase (currently mocked)
- Performing research on startups (placeholder for future implementation)
- API key authentication for secure access

## Project Structure

```
vc-research-engine/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Project dependencies
├── services/               # Service modules
│   ├── __init__.py         # Makes services a Python package
│   ├── crunchbase_service.py  # Service for Crunchbase data
│   └── research_service.py    # Service for research functionality
└── venv/                   # Python virtual environment
```

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
    "endpoints": ["/getData", "/research"],
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
- **Description**: Perform research on a startup (placeholder for future implementation)
- **Request Body**:
  ```json
  {
    "company_name": "OpenAI",
    "params": {
      "depth": "detailed"
    }
  }
  ```
- **Response Example**:
  ```json
  {
    "message": "Research functionality not yet implemented",
    "company": "OpenAI",
    "params": {
      "depth": "detailed"
    }
  }
  ```

## Future Enhancements

- Implement actual Crunchbase API integration
- Develop the research functionality
- Enhance authentication (dynamic API keys, user-based authentication)
- Add rate limiting
- Expand the API with additional endpoints
