import json
import os
import re
from typing import Dict, List, Optional, Any, Tuple, Union

import openai

async def chatbot_generate(user_query: str, input_json: Dict[str, Any]) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Process a user query using the OpenAI API and return a response with visualization data.
    
    Args:
        user_query: The user's question or request
        input_json: JSON data to use as context
        
    Returns:
        Tuple[str, Optional[Dict[str, Any]]]: Contains response text and optional visualization data
    """
    # Set your OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    openai.api_key = api_key
    
    # Create a system prompt that instructs the model how to respond
    system_prompt = """
    You are an AI assistant specialized in analyzing startup and venture capital data.
    Your task is to answer user queries about the provided JSON data and generate visualization data when appropriate.
    
    When generating a response, you should:
    1. Analyze the provided JSON data
    2. Answer the user's query based on that data
    3. Generate visualization data when it would enhance understanding
    
    Your response should be in JSON format with two main fields:
    - "response": A text response to the user's query
    - "visualization": (Optional) Data for creating a visualization, with the following structure:
        - "type": The chart type (bar_chart, line_chart, pie_chart, etc.)
        - "data": The chart data with "labels" and "datasets"
        - "options": Optional configuration for the chart
    
    Include the visualization field if a chart would be helpful for the query. 
    Be creative and try to connect any visualization to the query. For example if user asks about founding year, provide growth data for the whole history, if available.
    Make sure the visualization data is properly formatted for chart.js or similar libraries.
    """
    
    # Format the input JSON as a string for the prompt
    input_json_str = json.dumps(input_json, indent=2)
    
    # Create the user message with the query and data
    user_message = f"""
    User Query: {user_query}
    
    JSON Data:
    {input_json_str}
    
    Please provide a response with visualization data if appropriate. The text response should have as much context as possible, preferable 40 - 60 words long.
    """
    
    try:
        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4",  # Use an appropriate model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        
        # Extract the content from the response
        content = response.choices[0].message.content
        
        # Handle JavaScript functions in the response
        cleaned = re.sub(
            r'"callback":\s*function\s*\(.*?\}\s*', 
            '"callback": "function(value, index, values) { return \'$\' + value / 1e9 + \'B\'; }"', 
            content,
            flags=re.DOTALL
        )

        try:
            # Parse the JSON response
            parsed_response = json.loads(cleaned)
            
            # Extract the response text
            response_text = parsed_response.get("response", "No response provided")
            
            # Extract the visualization data if available
            visualization_data = parsed_response.get("visualization")
            
            # Return the tuple of response text and visualization data
            return response_text, visualization_data
            
        except json.JSONDecodeError:
            # If the response is not valid JSON, return it as plain text
            return f"Error parsing response as JSON. Raw response: {content}", None
            
    except Exception as e:
        # Handle any errors
        return f"Error processing your query: {str(e)}", None

# Mock data from CrunchbaseService
MOCK_DATA = {
    "openai": {
        "name": "OpenAI",
        "description": "OpenAI is an AI research and deployment company dedicated to ensuring that artificial general intelligence benefits all of humanity.",
        "funding_rounds": [
            {"date": "2019-03-01", "amount": 1000000000, "series": "A", "investors": ["Microsoft"]},
            {"date": "2021-01-15", "amount": 2000000000, "series": "B", "investors": ["Khosla Ventures", "Reid Hoffman"]}
        ],
        "founders": ["Sam Altman", "Elon Musk", "Greg Brockman", "Ilya Sutskever", "John Schulman", "Wojciech Zaremba"],
        "industry": "Artificial Intelligence",
        "founded_year": 2015,
        "total_funding": 3000000000,
        "website": "https://openai.com",
        "location": "San Francisco, CA",
        "status": "Operating"
    },
    "anthropic": {
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

async def run_interactive_demo():
    """
    Run an interactive demo of the chatbot functionality.
    """
    print("VC Research Engine Chatbot")
    print("=========================")
    
    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("\nWarning: OPENAI_API_KEY environment variable is not set.")
        print("Please set it before running this script:")
        print("export OPENAI_API_KEY='your-api-key'")
        return
    
    # Available companies in the mock data
    companies = list(MOCK_DATA.keys())
    print(f"\nAvailable companies in mock data: {', '.join(companies)}")
    
    # Get company name from user
    company_name = input("\nEnter a company name (or press Enter for 'openai'): ").strip().lower()
    if not company_name:
        company_name = "openai"
    
    # Get data for the company
    if company_name in MOCK_DATA:
        data = MOCK_DATA[company_name]
        print(f"\nUsing data for {data['name']}")
    else:
        print(f"\nAvailable companies in mock data: {', '.join(companies)}")
        data = {
            "name": company_name.capitalize(),
            "description": f"Mock data for {company_name}",
            "funding_rounds": [
                {"date": "2022-01-01", "amount": 5000000, "series": "Seed", "investors": ["Mock Ventures"]}
            ],
            "founders": ["Founder 1", "Founder 2"],
            "industry": "Technology",
            "founded_year": 2020,
            "total_funding": 5000000,
            "website": f"https://www.{company_name.lower()}.com",
            "location": "San Francisco, CA",
            "status": "Operating"
        }
        print(f"\nNo data found for {company_name}. Using generic mock data.")
    
    # Sample queries to demonstrate
    sample_queries = [
        f"How much funding has {data['name']} received?",
        f"Who are the founders of {data['name']}?",
        f"Show me the funding rounds of {data['name']}",
        f"Compare the funding amounts across different rounds for {data['name']}"
    ]
    
    print("\nSample queries you can try:")
    for i, query in enumerate(sample_queries, 1):
        print(f"{i}. {query}")
    
    # Interactive loop
    while True:
        # Get query from user
        print("\nEnter your query (or 'q' to quit, or a number 1-4 for sample queries):")
        user_input = input("> ").strip()
        
        # Check if user wants to quit
        if user_input.lower() in ['q', 'quit', 'exit']:
            break
        
        # Check if user entered a number for sample queries
        if user_input.isdigit() and 1 <= int(user_input) <= len(sample_queries):
            user_input = sample_queries[int(user_input) - 1]
            print(f"Using sample query: {user_input}")
        
        # Process the query
        print("\nProcessing query...")
        try:
            response_text, visualization_data = await chatbot_generate(user_input, data)
            
            # Display the response
            print("\n--- Response ---")
            print(response_text)
            
            # Display visualization data if available
            if visualization_data:
                print("\n--- Visualization Data ---")
                print(f"Type: {visualization_data.get('type')}")
                
                # Pretty print the visualization data
                print(json.dumps(visualization_data, indent=2))
        except Exception as e:
            print(f"\nError: {str(e)}")

# Run the interactive demo if this script is executed directly
if __name__ == "__main__":
    import asyncio
    
    # Run the interactive demo
    asyncio.run(run_interactive_demo())
