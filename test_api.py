import asyncio
import json
import websockets
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
API_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-12345"
WS_URL = "ws://localhost:8000/ws/research"

async def test_root_endpoint():
    """Test the root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200

async def test_get_data_endpoint():
    """Test the getData endpoint"""
    print("\n=== Testing getData Endpoint ===")
    headers = {"X-API-Key": API_KEY}
    data = {"company_name": "OpenAI"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/getData",
            headers=headers,
            json=data
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200

async def test_research_endpoint():
    """Test the research endpoint"""
    print("\n=== Testing Research Endpoint ===")
    headers = {"X-API-Key": API_KEY}
    data = {
        "company_name": "Anthropic",
        "params": {
            "depth": "standard"
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/research",
            headers=headers,
            json=data
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200

async def test_websocket_endpoint():
    """Test the WebSocket endpoint"""
    print("\n=== Testing WebSocket Endpoint ===")
    
    # Initial message with API key and company name
    initial_message = {
        "api_key": API_KEY,
        "company_name": "Anthropic",
        "params": {
            "depth": "standard"
        }
    }
    
    try:
        async with websockets.connect(WS_URL) as websocket:
            # Send initial message
            await websocket.send(json.dumps(initial_message))
            print(f"Sent: {json.dumps(initial_message)}")
            
            # Listen for messages
            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=60)
                    message_data = json.loads(message)
                    
                    print(f"Received: {message_data['type']}")
                    
                    if message_data["type"] == "progress" or message_data["type"] == "tool":
                        print(f"  {message_data['message']}")
                    
                    if message_data["type"] == "result":
                        print(f"  Result received with {len(message_data['data'].get('dashboard_components', []))} components")
                        return True
                    
                    if message_data["type"] == "error":
                        print(f"  Error: {message_data['message']}")
                        return False
                    
                except asyncio.TimeoutError:
                    print("Timeout waiting for response")
                    return False
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("=== Starting API Tests ===")
    
    # Test root endpoint
    root_success = await test_root_endpoint()
    
    # Test getData endpoint
    get_data_success = await test_get_data_endpoint()
    
    # Test research endpoint
    research_success = await test_research_endpoint()
    
    # Ask user if they want to test the WebSocket endpoint
    print("\nDo you want to test the WebSocket endpoint? This may take a few minutes. (y/n)")
    choice = input().lower()
    
    websocket_success = None
    if choice == 'y':
        # Test WebSocket endpoint
        websocket_success = await test_websocket_endpoint()
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Root Endpoint: {'✅ Success' if root_success else '❌ Failed'}")
    print(f"getData Endpoint: {'✅ Success' if get_data_success else '❌ Failed'}")
    print(f"Research Endpoint: {'✅ Success' if research_success else '❌ Failed'}")
    
    if websocket_success is not None:
        print(f"WebSocket Endpoint: {'✅ Success' if websocket_success else '❌ Failed'}")
    else:
        print("WebSocket Endpoint: Not tested")

if __name__ == "__main__":
    asyncio.run(main())
